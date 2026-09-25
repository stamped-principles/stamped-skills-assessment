# First implementation: decisions and concerns

## What this iteration establishes

The first model separates the object, its intended use, the rubric, the assessment, and subsequent reviews.
It uses LinkML as the editable schema source, generates five closed JSON Schemas, and adds cross-record checks in a small offline Python library.
Pinned principles and checklist resources travel with the installed package.
The parallel agent repository distributes one assessor skill through APM, with agent-specific resources inside that skill directory.
Neither runtime depends on Skills Workshop.

Comprehensiveness is represented by planned evidence activities for each criterion.
Resource limits, permissions, assistance, access barriers, and observed effort are separate fields.
This permits an assessment to explain why an activity remains unfinished without equating that barrier with a failure of the object.
The finalized report accounts for the plan; the derived scope completion flag states whether all planned activities were actually completed.

The pilot examines a fixed STAMPED paper revision.
Its seven criteria cover selected concerns across the seven principles.
It completes seven inspections and explicitly leaves two retrieval activities unattempted.
It is a useful exercise of the records, not evidence of full checklist coverage, reproducibility, or assessor-skill effectiveness.
Priorities were inferred by the assessor and need human calibration.

## Concerns that emerged

### Rubric quality determines what a positive judgment means

A narrow criterion can be demonstrated while a principle remains largely unexamined.
The pilot's modularity judgment establishes a separate author-rendering target, not full modularity of the research object.
Summaries therefore retain criterion counts, mapped checklist counts, and explicit scope.
Mapped items are references, not counts of checklist items passed.
There is no overall score.

Use-case priorities must not become a way to hide inconvenient requirements.
Each principle retains its own rationale and priority, including exclusions.
The next rubric iteration should separate component-specific targets more precisely, particularly durable outputs and disposable execution environments.
The current model supports object composition and textual targets but does not yet formally bind each criterion to a particular component.

### Validation cannot establish truth

The validator catches missing evidence references, mismatched criteria, stale reviews, mutable source revisions, and inconsistent activity claims.
It cannot establish that a cited resource was actually inspected, that an observation is accurate, or that a judgment is justified.
Evidence quality and rubric adequacy require review and eventually independent checks.
Public evidence references can also disappear; content hashes identify bytes but do not preserve their availability.

### Review automation needs calibration

The queue emphasizes disagreement, unresolved essential criteria, and initial human review of each rubric criterion.
After calibration it retains deterministic sampling.
This is a provisional operational policy; it has no measured recall for consequential errors.
Agreement among agents may reflect shared assumptions rather than correctness.
Reviewer identities in YAML are claims; Git contribution review supplies the initial trust boundary.
Separate reviews preserve disagreement without rewriting the assessment being challenged.

SHACL Vue deserves a focused round-trip experiment.
Orinoco's editor also relies on RDF resources, deployment, and authenticated GitHub handoff.
Adopting it should follow a demonstration that nested observations, review references, and semantic digests survive editing correctly.
The generated Markdown review report is the immediate human interface.

### Skill improvement needs a different experimental design

An artifact assessment records what an assessor concluded under stated conditions.
It does not establish that using the skill improved those conclusions.
A useful next experiment compares repeated assessments of the same snapshots and rubrics with and without the skill, holding resources and permissions as steady as practical.
Independent human adjudication should examine correctness, missed evidence, unjustified confidence, and workload.
The comparison and intervention fields can retain that context; a full experiment schema is deferred.

### Distribution and evolution need explicit boundaries

APM installs instructions and agent resources; the Python package installs validation and bundled schema resources.
The skill pins its executable dependency to an exact assessment repository revision.
This avoids tying consumers to Workshop while allowing each repository to evolve independently.
Version 0.1 accepts one model and reference bundle.
Before changing that contract, decide how old assessments remain readable and how migrations preserve review identities.
Review digests currently cover the assessment record itself; the referenced rubric, object, and use case must retain their published identities and content.
Git review must enforce that immutability in this prototype.
Transitive context digests or a history-aware validation check would make that protection more robust.
There is no collection endpoint, hosted review editor, or tagged production release in this iteration.

## Suggested next iteration

1. Review the pilot rubric and a few prioritized judgments together.
2. Add a data-journalism use case to expose assumptions inherited from computational research.
3. Add explicit component targets if that review confirms the need.
4. Perform one comprehensive assessment with actual retrieval and execution under agreed permissions.
5. Compare independent assessors before selecting an aggregation or scoring model.
6. Trial a schema-derived review form against the same Git records.
