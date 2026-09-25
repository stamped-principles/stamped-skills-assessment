"""Offline record validation and reproducible assessment summaries."""
from collections import Counter
from hashlib import sha256
from importlib.resources import files
import json
import math
from pathlib import Path
import re

import jsonschema
import yaml

DATA = files('stamped_assessment').joinpath('data')
KINDS = ('use_case', 'object', 'rubric', 'assessment', 'review')


class InvalidStore(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise InvalidStore(f'duplicate YAML key: {key}')
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
# Keep ISO dates as strings, as required by JSON Schema.
UniqueLoader.yaml_implicit_resolvers = {
    key: [(tag, rx) for tag, rx in values if tag != 'tag:yaml.org,2002:timestamp']
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def digest(record):
    return sha256(json.dumps(record, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=False).encode()).hexdigest()


def schema(kind):
    if kind not in KINDS:
        raise InvalidStore(f'unknown record type: {kind}')
    return json.loads(DATA.joinpath('generated', f'{kind}.schema.json').read_text())


def references():
    root = DATA.joinpath('upstream')
    lock = json.loads(root.joinpath('lock.json').read_text())
    for item in lock['sources']:
        if sha256(root.joinpath(item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise InvalidStore(f'upstream checksum mismatch: {item["path"]}')
    principles = json.loads(root.joinpath('principles/stamped-principles.json').read_text())
    checklist = json.loads(root.joinpath('checklist/stamped-checklist.json').read_text())
    if (principles['version'] != lock['principles_version'] or
            checklist['checklist_version'] != lock['checklist_version'] or
            checklist['principles_version'] != principles['version'] or
            checklist['schema_version'] != lock['checklist_schema_version']):
        raise InvalidStore('incompatible upstream versions')
    codes = {p['code']: p['category'] for p in principles['principles']}
    items = {}
    for group in checklist['data']:
        for entry in group['entries']:
            categories = {codes[c] for c in entry['principle_codes']}
            for item in entry['items']:
                if item['id'] in items:
                    raise InvalidStore('duplicate upstream checklist item')
                items[item['id']] = {'categories': categories, 'level': group['level']}
    return lock, set(codes.values()), items


def require(condition, message):
    if not condition:
        raise InvalidStore(message)


def indexed(values, key, label):
    result = {v[key]: v for v in values}
    require(len(result) == len(values), f'duplicate {label}')
    return result


def validate(records):
    lock, categories, checklist = references()
    for record in records:
        require(isinstance(record, dict), 'record must be a mapping')
        kind = record.get('record_type')
        try:
            jsonschema.validate(record, schema(kind), format_checker=jsonschema.FormatChecker())
        except jsonschema.ValidationError as exc:
            raise InvalidStore(f'{record.get("id", "?")}: {exc.message}') from exc
        def nonempty(value):
            if isinstance(value, str):
                require(bool(value.strip()), 'blank strings are not valid record values')
            elif isinstance(value, float):
                require(math.isfinite(value), 'non-finite numbers are not valid record values')
            elif isinstance(value, dict):
                for child in value.values():
                    nonempty(child)
            elif isinstance(value, list):
                for child in value:
                    nonempty(child)
        nonempty(record)
    db = indexed(records, 'id', 'record identifier')

    def ref(identifier, kind):
        require(identifier in db, f'missing {kind}: {identifier}')
        require(db[identifier]['record_type'] == kind, f'wrong record type: {identifier}')
        return db[identifier]

    def source(s):
        require(bool(s.get('revision') or s.get('sha256')), 'source needs an immutable revision or digest')
        if s.get('revision'):
            require(bool(re.fullmatch(r'[a-f0-9]{40}|[a-f0-9]{64}', s['revision'])), 'revision must be a full Git commit; use sha256 for other snapshots')

    for r in records:
        kind = r['record_type']
        if kind in ('object', 'rubric'):
            ref(r['use_case'], 'use_case')
        if kind == 'object':
            require(bool(r['sources']), 'object needs at least one source')
            for s in r['sources']:
                source(s)
            for child in r.get('components', []):
                ref(child, 'object')
                require(child != r['id'], 'object cannot contain itself')
        elif kind == 'rubric':
            require(r['reference_bundle'] == lock['id'], 'unsupported reference bundle')
            aims = indexed(r['principles'], 'category', 'principle aim')
            require(set(aims) == categories, 'rubric must address all seven principles')
            criteria = indexed(r['criteria'], 'id', 'criterion')
            require(bool(criteria), 'rubric must have criteria')
            for c in criteria.values():
                require(bool(c['required_activities']), 'criterion must declare required activities')
                require(len(set(c['required_activities'])) == len(c['required_activities']), 'duplicate activity')
                for item in c.get('checklist_items', []):
                    require(item in checklist, f'unknown checklist item: {item}')
                    require(c['category'] in checklist[item]['categories'], f'checklist category mismatch: {item}')
            for category, aim in aims.items():
                require(aim['priority'] == 'out_of_scope' or any(c['category'] == category for c in criteria.values()),
                        f'active principle has no criteria: {category}')
        elif kind == 'assessment':
            obj = ref(r['object'], 'object')
            rubric = ref(r['rubric'], 'rubric')
            require(obj['use_case'] == rubric['use_case'], 'object/rubric use case mismatch')
            if r['assessor'].get('skill'):
                source(r['assessor']['skill'])
            criteria = {c['id']: c for c in rubric['criteria']}
            plan = indexed(r['plan'], 'criterion', 'planned criterion')
            require(set(plan) == set(criteria), 'plan must account for every rubric criterion')
            for key, check in plan.items():
                require(set(criteria[key]['required_activities']) <= set(check['activities']),
                        f'plan omits required activity: {key}')
                require(len(check['activities']) == len(set(check['activities'])), 'duplicate planned activity')
            observations = indexed(r.get('observations', []), 'id', 'observation')
            for o in observations.values():
                require(o['criterion'] in plan and o['activity'] in plan[o['criterion']]['activities'],
                        'observation outside declared plan')
                if o['status'] == 'completed':
                    require(bool(o.get('evidence')), 'completed activity needs inspectable evidence')
                    require(not o.get('barrier'), 'completed activity cannot also be blocked')
                if o['status'] == 'blocked':
                    require(bool(o.get('barrier')), 'blocked activity needs a barrier')
            judgments = indexed(r.get('judgments', []), 'criterion', 'judgment')
            require(set(judgments) <= set(criteria), 'judgment references unknown criterion')
            for j in judgments.values():
                require(bool(j['observations']), 'judgment needs observations')
                require(len(set(j['observations'])) == len(j['observations']), 'duplicate observation reference')
                for oid in j['observations']:
                    require(oid in observations and observations[oid]['criterion'] == j['criterion'],
                            'judgment evidence belongs to another criterion or is missing')
                if j['status'] in ('demonstrated', 'partial', 'not_demonstrated'):
                    require(any(observations[i]['status'] == 'completed' for i in j['observations']),
                            'substantive judgment requires a completed observation')
                if j['status'] == 'demonstrated':
                    completed = {observations[i]['activity'] for i in j['observations']
                                 if observations[i]['status'] == 'completed'}
                    require(set(criteria[j['criterion']]['required_activities']) <= completed,
                            'demonstrated judgment lacks required activity evidence')
            summaries = indexed(r.get('principle_summaries', []), 'category', 'principle summary')
            if r['status'] == 'finalized':
                require(bool(r.get('finished_at')), 'finalized assessment needs finish time')
                require(set(judgments) == set(criteria), 'finalized assessment needs every judgment')
                require(set(summaries) == categories, 'finalized assessment needs seven summaries')
                observed = {(o['criterion'], o['activity']) for o in observations.values()}
                require(all((k, a) in observed for k, p in plan.items() for a in p['activities']),
                        'finalized assessment must account for every planned activity')
            if r.get('supersedes'):
                previous = ref(r['supersedes'], 'assessment')
                require(previous['id'] != r['id'], 'assessment cannot supersede itself')
                require((previous['object'], previous['rubric']) == (r['object'], r['rubric']),
                        'assessment correction must retain object and rubric; use comparison_group for a changed target')
        elif kind == 'review':
            a = ref(r['assessment'], 'assessment')
            require(r['assessment_sha256'] == digest(a), 'review targets a changed assessment')
            decisions = indexed(r['decisions'], 'criterion', 'review decision')
            require(bool(decisions), 'review needs decisions')
            require(set(decisions) <= {j['criterion'] for j in a.get('judgments', [])}, 'review targets missing judgment')
            if r.get('supersedes'):
                previous = ref(r['supersedes'], 'review')
                require(previous['assessment'] == r['assessment'] and previous['id'] != r['id'], 'invalid review supersession')
                require((previous['reviewer']['name'], previous['reviewer']['kind']) ==
                        (r['reviewer']['name'], r['reviewer']['kind']), 'a reviewer cannot supersede another reviewer')

    def acyclic(kind, edges):
        done, visiting = set(), set()
        def visit(key):
            require(key not in visiting, f'cycle in {kind}: {key}')
            if key in done:
                return
            visiting.add(key)
            for child in edges(db[key]):
                visit(child)
            visiting.remove(key)
            done.add(key)
        for key, r in db.items():
            if r['record_type'] == kind:
                visit(key)
    acyclic('object', lambda r: r.get('components', []))
    for kind in ('assessment', 'review'):
        acyclic(kind, lambda r: [r['supersedes']] if r.get('supersedes') else [])
    return db


def load(path):
    root = Path(path)
    require(root.is_dir(), f'store directory does not exist: {root}')
    records = []
    for p in sorted(root.rglob('*')):
        if p.suffix in ('.yaml', '.yml', '.json'):
            try:
                records.append(yaml.load(p.read_text(), Loader=UniqueLoader))
            except (yaml.YAMLError, InvalidStore) as exc:
                raise InvalidStore(f'{p}: {exc}') from exc
    require(bool(records), 'store contains no records')
    return validate(records)


def summarize(db, assessment):
    rubric = db[assessment['rubric']]
    observations = assessment.get('observations', [])
    planned = {(p['criterion'], a) for p in assessment['plan'] for a in p['activities']}
    observed = {(o['criterion'], o['activity']) for o in observations}
    completed = {(o['criterion'], o['activity']) for o in observations if o['status'] == 'completed'}
    report = {'assessment': assessment['id'], 'assessment_sha256': digest(assessment),
              'rubric': rubric['id'], 'reference_bundle': rubric['reference_bundle'],
              'record_status': assessment['status'],
              'planned_activities': len(planned), 'accounted_activities': len(observed & planned),
              'completed_activities': len(completed & planned),
              'scope_accounted_for': planned <= observed, 'scope_completed': planned <= completed,
              'observation_counts': dict(Counter(o['status'] for o in observations)), 'principles': []}
    criteria = {c['id']: c for c in rubric['criteria']}
    _, _, checklist = references()
    for aim in rubric['principles']:
        relevant = [j for j in assessment.get('judgments', []) if criteria[j['criterion']]['category'] == aim['category']]
        mapped = {i for c in criteria.values() if c['category'] == aim['category'] for i in c.get('checklist_items', [])}
        report['principles'].append({**aim, 'criterion_count': sum(c['category'] == aim['category'] for c in criteria.values()),
                                     'checklist_items_mapped': len(mapped),
                                     'checklist_items_available': sum(aim['category'] in c['categories'] for c in checklist.values()),
                                     'judgment_counts': dict(Counter(j['status'] for j in relevant))})
    return report


def review_queue(db, sample_percent=10):
    require(0 <= sample_percent <= 100, 'sample percent must be between 0 and 100')
    superseded = {r['supersedes'] for r in db.values() if r.get('supersedes')}
    reviews = [r for r in db.values() if r['record_type'] == 'review' and r['id'] not in superseded]
    assessments = [a for a in db.values() if a['record_type'] == 'assessment' and a['id'] not in superseded]
    queue = []
    for a in assessments:
        rubric = db[a['rubric']]
        criteria = {c['id']: c for c in rubric['criteria']}
        aims = {p['category']: p for p in rubric['principles']}
        for j in a.get('judgments', []):
            cid = j['criterion']
            decisions = [(r, d) for r in reviews if r['assessment'] == a['id']
                         for d in r['decisions'] if d['criterion'] == cid]
            reasons = []
            if any(d['disposition'] != 'agree' for _, d in decisions):
                reasons.append('review_disagreement_or_missing_evidence')
            if any(other['object'] == a['object'] and other['rubric'] == a['rubric'] and other['id'] != a['id']
                   and any(x['criterion'] == cid and x['status'] != j['status'] for x in other.get('judgments', []))
                   for other in assessments):
                reasons.append('assessors_disagree')
            human_agrees = any(r['reviewer']['kind'] == 'human' and d['disposition'] == 'agree' for r, d in decisions)
            if not human_agrees:
                if j['status'] in ('unknown', 'partial', 'not_demonstrated') and aims[criteria[cid]['category']]['priority'] == 'essential':
                    reasons.append('unresolved_essential_criterion')
                if not any(db[r['assessment']]['rubric'] == rubric['id'] and r['reviewer']['kind'] == 'human'
                           and any(d['criterion'] == cid for d in r['decisions']) for r in reviews):
                    reasons.append('criterion_has_no_human_review')
                if int(sha256(f'{a["id"]}:{cid}'.encode()).hexdigest(), 16) % 100 < sample_percent:
                    reasons.append('deterministic_sample')
            if reasons:
                high = any(x in reasons for x in ('review_disagreement_or_missing_evidence', 'assessors_disagree', 'unresolved_essential_criterion'))
                queue.append({'assessment': a['id'], 'assessment_sha256': digest(a), 'criterion': cid,
                              'priority': 'high' if high else 'normal', 'reasons': reasons})
    return sorted(queue, key=lambda x: (x['priority'] != 'high', x['assessment'], x['criterion']))


def review_report(db, limit=20):
    """A generated reading aid; decisions remain separate review records."""
    require(limit > 0, 'review report limit must be positive')
    queue = review_queue(db)
    lines = ['# STAMPED review queue', '',
             f'Showing {min(limit, len(queue))} of {len(queue)} queued judgments.',
             'These are assessor assertions awaiting review, not human approvals.', '']
    for entry in queue[:limit]:
        a = db[entry['assessment']]
        rubric = db[a['rubric']]
        c = next(c for c in rubric['criteria'] if c['id'] == entry['criterion'])
        j = next(j for j in a['judgments'] if j['criterion'] == c['id'])
        lines += [f'## {a["id"]}: {c["id"]}', '',
                  f'Priority: {entry["priority"]}. Reasons: {", ".join(entry["reasons"])}.',
                  f'Assessment digest: `{entry["assessment_sha256"]}`', '',
                  f'Question: {c["question"]}', f'Target: {c["target"]}',
                  f'Judgment: **{j["status"]}**. {j["rationale"]}', '']
        for o in a.get('observations', []):
            if o['id'] in j['observations']:
                lines += [f'- {o["activity"]}: {o["status"]}. {o["description"]}']
                for e in o.get('evidence', []):
                    lines += [f'  Evidence: {e["uri"]} ({e["description"]})']
        lines += ['', 'Record agreement, disagreement, or a request for evidence in a separate review record.', '']
    return '\n'.join(lines)
