# STAMPED assessments

A working foundation for assessing digital and research objects in their intended use cases.
The repository stores versioned rubrics, evidence, assessments, and separate reviews as YAML.
The Python package provides offline validation, per-principle summaries, and a review queue.
It has no dependency on Skills Workshop, an account service, or a hosted endpoint.

## Start

With Pixi installed:

```sh
pixi install --locked
pixi run validate
pixi run stamped-assess summarize records
pixi run review
pixi run stamped-assess review-report records
```

The package can also be installed with `python -m pip install .`.
The installed `stamped-assess` command includes its generated JSON Schemas and pinned STAMPED reference data.
It does not fetch or execute assessment evidence.

## Records

- `use_case`: objective, audience, and intended use
- `object`: exact source snapshot, boundary, and optional component snapshots
- `rubric`: principle priorities, desired direction, and observable criteria
- `assessment`: declared activities, available resources, observations, judgments, and seven principle summaries
- `review`: item-specific decisions tied to the assessment's semantic SHA-256

The [LinkML model](src/stamped_assessment/data/schemas/assessment.yaml) defines these five record schemas.
JSON Schemas are generated from that model and shipped in the package.
Cross-record and evidence consistency rules are checked separately by the validator.
The [reference lock](src/stamped_assessment/data/upstream/lock.json) identifies the exact upstream principles and checklist files and their checksums.
The checklist is a guide; a rubric can add criteria that are important for its use case.

See [the design](docs/design.md), [contribution workflow](docs/contributing-assessments.md), and [development notes](docs/development.md).
The [implementation report](docs/implementation-report.md) records decisions, concerns, and next experiments.

## Initial evidence

`records/` contains an unreviewed inspection pilot of the STAMPED paper at a fixed commit.
It exercises the record design; it is not a comprehensive assessment of the manuscript or evidence that the new assessor skill is effective.
The rubric priorities were inferred by the assessor and are explicitly marked as such.
Retrieval and reproduction were not performed.
There are no human review records yet.

## Licensing and provenance

New code is MIT licensed; schemas, documentation, and assessment records are CC-BY-4.0.
Vendored principles and checklist materials retain their upstream CC-BY-4.0 license and source attribution in the reference lock.
BIDS Schema Tools informed the separation of schema resources, validation, optional development tooling, and a small CLI; no BIDS code is copied.
