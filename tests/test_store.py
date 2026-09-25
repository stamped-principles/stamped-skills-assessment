from copy import deepcopy
from pathlib import Path

import pytest

from stamped_assessment.store import InvalidStore, digest, load, review_queue, summarize, validate

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def records():
    return deepcopy(list(load(ROOT / 'records').values()))


def assessment(records):
    return next(r for r in records if r['record_type'] == 'assessment')


def review(a, **kwargs):
    return {'id': 'test-review', 'record_type': 'review', 'schema_version': '0.1.0',
            'assessment': a['id'], 'assessment_sha256': digest(a),
            'reviewer': {'name': 'Synthetic test reviewer', 'kind': 'human'},
            'created_at': '2026-09-25T22:00:00Z',
            'decisions': [{'criterion': a['judgments'][0]['criterion'],
                           'disposition': 'agree', 'rationale': 'Synthetic fixture only.'}], **kwargs}


def test_finalized_is_not_comprehensive(records):
    db = validate(records)
    summary = summarize(db, assessment(records))
    assert summary['record_status'] == 'finalized'
    assert summary['scope_accounted_for'] is True
    assert summary['scope_completed'] is False
    assert summary['completed_activities'] < summary['planned_activities']
    assert 'score' not in summary


def test_positive_judgment_requires_required_evidence(records):
    assessment(records)['judgments'][0]['status'] = 'demonstrated'
    with pytest.raises(InvalidStore, match='required activity'):
        validate(records)


def test_missing_observation_is_not_hidden_by_finalization(records):
    assessment(records)['observations'].pop()
    with pytest.raises(InvalidStore):
        validate(records)


def test_unknown_checklist_identifier_rejected(records):
    next(r for r in records if r['record_type'] == 'rubric')['criteria'][0]['checklist_items'] = ['invented']
    with pytest.raises(InvalidStore, match='unknown checklist'):
        validate(records)


def test_blocked_activity_requires_explanation(records):
    a = assessment(records)
    o = next(o for o in a['observations'] if o['status'] == 'not_attempted')
    o['status'] = 'blocked'
    with pytest.raises(InvalidStore, match='barrier'):
        validate(records)
    o['barrier'] = {'kind': 'access', 'detail': 'Account required.',
                    'next_action': 'Ask an authorized recipient.', 'user_help_needed': True}
    validate(records)


def test_review_detects_changed_assessment(records):
    a = assessment(records)
    records.append(review(a))
    a['judgments'][0]['rationale'] += ' Revised.'
    with pytest.raises(InvalidStore, match='changed assessment'):
        validate(records)


def test_review_does_not_rewrite_judgments(records):
    a = assessment(records)
    original = deepcopy(a)
    r = review(a)
    r['decisions'][0]['disposition'] = 'disagree'
    records.append(r)
    queue = review_queue(validate(records), 0)
    assert a == original
    assert any('review_disagreement_or_missing_evidence' in q['reasons'] for q in queue)


def test_duplicate_record_identifier_rejected(records):
    records.append(deepcopy(records[0]))
    with pytest.raises(InvalidStore, match='duplicate record'):
        validate(records)


def test_object_cycle_rejected(records):
    obj = next(r for r in records if r['record_type'] == 'object')
    child = deepcopy(obj)
    child['id'] = 'child'
    child['components'] = [obj['id']]
    obj['components'] = ['child']
    records.append(child)
    with pytest.raises(InvalidStore, match='cycle'):
        validate(records)


def test_no_mutable_revision(records):
    next(r for r in records if r['record_type'] == 'object')['sources'][0]['revision'] = 'main'
    with pytest.raises(InvalidStore, match='full Git commit'):
        validate(records)


def test_duplicate_yaml_keys_rejected(tmp_path):
    (tmp_path / 'bad.yaml').write_text('id: one\nid: two\n')
    with pytest.raises(InvalidStore, match='duplicate YAML key'):
        load(tmp_path)


def test_unknown_fields_rejected(records):
    assessment(records)['unmodeled'] = 'not silently ignored'
    with pytest.raises(InvalidStore):
        validate(records)


def test_calibration_review_is_per_criterion(records):
    records.append(review(assessment(records)))
    q = review_queue(validate(records), 0)
    assert any('criterion_has_no_human_review' in x['reasons'] for x in q)


def test_peer_disagreement_is_queued(records):
    a = deepcopy(assessment(records))
    a['id'] = 'independent-assessment'
    a['judgments'][0]['status'] = 'partial'
    records.append(a)
    q = review_queue(validate(records), 0)
    assert any('assessors_disagree' in x['reasons'] for x in q)


def test_agent_cannot_supersede_human_review(records):
    human = review(assessment(records))
    agent = deepcopy(human)
    agent.update(id='agent-review', supersedes=human['id'])
    agent['reviewer'] = {'name': 'Agent', 'kind': 'agent'}
    records.extend([human, agent])
    with pytest.raises(InvalidStore, match='another reviewer'):
        validate(records)


def test_assessment_schema_version_is_explicit(records):
    assessment(records)['schema_version'] = '99.0.0'
    with pytest.raises(InvalidStore):
        validate(records)


def test_checklist_mapping_counts_do_not_claim_full_coverage(records):
    report = summarize(validate(records), assessment(records))
    assert any(p['checklist_items_mapped'] < p['checklist_items_available'] for p in report['principles'])
