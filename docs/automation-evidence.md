# Learning from instrumented skill use

The AutoHarness completion-hook trial supplies useful cases for STAMPED assessment design.
It does not establish that reflection improves task results.
This note transfers lessons into assessment practice and defines a small evaluation pilot; it does not introduce a shared schema or a dependency on AutoHarness or Skills Workshop.

## Evidence from the implementation

The inspected implementation is [AutoHarness commit 19be975](https://github.com/leej3/autoharness/tree/19be975342843ead997491beba31fe55100d21c7/native-skills/skills/autoharness-reflect).
Its [hook guide](https://github.com/leej3/autoharness/blob/19be975342843ead997491beba31fe55100d21c7/native-skills/skills/autoharness-reflect/references/completion-hooks.md) distinguishes host events from agent reports and documents collection gaps.
The following are implementation properties, not measurements of live deployment coverage:

| Mechanism | What it supports | What remains unestablished |
|---|---|---|
| A tool argument mentions a skill path | A candidate for subsequent confirmation | Whether the skill was read successfully or materially used |
| A Stop event | A turn ended | Whether the task succeeded or an assessed criterion was demonstrated |
| An agent confirms use and success | A named agent's assertion about its work | Independent correctness, user satisfaction, or causal benefit |
| Start and end timestamps | Elapsed turn time, including waits | Time attributable to one skill or assessment activity |
| Validated JSONL and retry identifiers | Structurally checked records with deduplication keys | Complete delivery, independent trials, or preservation of all context |
| Installation and isolated tests | Behavior in the tested environment | Host activation, trusted hook execution, or coverage of real tasks |

The hook records unknown outcomes for host events and null duration when the start event is absent.
Consumers must deduplicate by `(kind, id)` because a crash between append and state update can repeat a record.
Candidate detection can miss earlier-turn reads and indirect paths.
The compact telemetry does not retain enough task, instrument, or evidence provenance to serve by itself as a reproducible assessment.

## Apply the distinctions in STAMPED

Keep collection, observation, judgment, and review separate.
An assessment may cite a host event as evidence, but its judgment still needs a criterion-specific explanation.
An agent's success report remains an assertion even when it passes schema validation.
Separate review records retain disagreements and corrections without rewriting the original claim.

| Question | Existing representation | Necessary qualification |
|---|---|---|
| What was assessed? | Object sources and component boundaries | Pin the assessed artifact separately from the collector and assessor |
| Who reached the conclusion? | Assessor and reviewer actors | Describe an external evidence producer in the evidence description; do not replace the assessor identity with the collector |
| What actually happened? | Planned checks, observations, evidence | A detected path is not a completed execution or confirmed use |
| Why is evidence missing? | Conditions, blocked or not_attempted observations, barriers | Record a barrier only when established; absence of telemetry alone is not a failed object |
| How much work was measured? | Observation elapsed_seconds; assessment start/end | Only assign a duration to the activity it actually measures |
| What was concluded? | Criterion judgments and principle summaries | Process success does not imply a positive judgment across principles |
| What changed? | New versions, supersedes, comparison_group | Distinguish changes to the object from changes to the assessor or instrument |

For example, inspectable hook installation can complete an inspection criterion while live-delivery testing remains not_attempted.
If a delivery attempt establishes a trust restriction, describe that restriction and the next authorized action as a barrier.
Do not infer either successful delivery or object failure from an empty event store.
When required evidence is unavailable, an unknown judgment can be the correct result.

Collector errors, assessor mistakes, and object defects require different remedies.
A harness rejecting a report does not establish a defect in the research object.
Fixing a skill instruction changes the assessment instrument; it does not retrospectively strengthen evidence about the object.
The assessment intervention field describes changes between object versions; document an experimental instrument change in the evaluation protocol instead.

## Preserve context without expanding every record

For an assessment that uses automation evidence, attach a small, versioned evidence manifest when the source records lack necessary context.
Include only information needed to interpret the claim: task or trial identity, artifact and instrument revisions, collection method and known gaps, relevant configuration and permissions, timing scope, and evidence locators and digests.
Record the actual model/runtime and skill revision on the assessor when known.
The current model has no dedicated per-observation producer or collector-configuration fields; use an evidence description and a referenced manifest rather than pretending those fields already exist.
The manifest need not follow the telemetry schema.

A review's assessment digest binds the assessment content, not the bytes of every linked resource.
Pin supporting resources and preserve the material needed for later review where permitted.
A digest establishes identity when bytes are available; it does not make them retrievable.
If evidence must be redacted, identify the shareable derivative and its digest separately from the restricted original, and state what a reviewer cannot verify.
Keep sensitive content and classification reasons in an access-controlled overlay without making the standalone assessment tools depend on that overlay.

## Count coverage before interpreting outcomes

Declare the unit being counted: task, turn, confirmed skill use, assessment, criterion, or review decision.
A task can span several turns and agents; several records can describe the same event.
Retried delivery and linked Workshop feedback are not independent observations.
Do not sum overlapping turn, skill, or subagent durations as total wall time.
Missing measurements remain unknown rather than zero.

Report numerators with their denominators and selection method.
Useful distinctions include eligible tasks, tasks with verified collection, candidate turns, confirmed uses, criteria with sufficient evidence, and independently reviewed decisions.
An instrument cannot establish how many events it missed solely from the events it captured.
Use a separately enumerated pilot task list or explicit usage markers to estimate coverage.
The current STAMPED summaries count recorded activities and judgments; they do not measure collector recall or deduplicate external telemetry.

Review a sample of quiet successes and high-confidence positive judgments as well as disagreements and unresolved essential criteria.
Agreement can reflect shared blind spots.
The current review queue is a prioritization aid, not a calibrated estimate of error detection.
Retain the sampling rule, sampling frame, and unreviewed cases when reporting review findings.

## A small evaluation pilot

This is a proposed experiment, not a completed evaluation.
Run it through ordinary native agent tasks with isolated fixtures; no general execution platform is required.
First fix the object snapshots, rubric, task instructions, relevant permissions, and expected evidence before comparing assessor behavior.
The following cases exercise reasoning that structural validators alone cannot establish:

| Fixture condition | Expected assessment behavior |
|---|---|
| Skill path appears only in a failed read or installation | Treat it as a candidate, not confirmed material use |
| Hook installed; no verified host events | Separate installation evidence from unverified delivery |
| Duplicate event and matching feedback record | Count one underlying event, retaining both sources |
| Missing start or overlapping agent intervals | Leave unavailable activity timing unknown; avoid summing overlapping wall time |
| Tool exits successfully but output violates the criterion | Report completed execution and the criterion-specific negative finding separately |
| Collector fails while object evidence remains available | Attribute the collector failure correctly and assess available evidence |
| Two agents agree on a claim with inadequate evidence | Preserve the agreement without treating it as independent verification |
| A linked resource changes after review | Expose the provenance gap instead of claiming the old digest binds the changed resource |

Compare an assessor using the current evidence bundle with one given clearly attributed telemetry; test additional explicit usage markers as a separate condition if coverage remains a problem.
Hold the object, rubric, model, tools, permissions, and task limits equivalent, pin each treatment, vary execution order, and repeat trials.
Separate grading from execution and hide treatment labels from reviewers where practical.
Label agent grading as agent grading; obtain human adjudication for a calibration sample rather than assuming agent agreement establishes truth.

Predeclare per-criterion measures: unsupported positive judgments, unjustified negative judgments, missed evidence, correct handling of unknowns, correction burden, and measured assessment/review time.
Report sample sizes, exclusions, uncertainty, and collection coverage alongside results.
Keep these evaluation measures separate from the object's seven STAMPED principle summaries; do not create a universal adherence score.
One successful smoke test supports functionality in that fixture, not comparative effectiveness.

## Priorities for the next assessment

1. Apply evidence attribution, missing-data handling, and timing scope in the assessor instructions now.
2. Run the small pilot before making benefit claims or changing review-queue priorities based on telemetry.
3. Add collection fields only to answer observed gaps: instrument identity, explicit use markers, and corrections captured when they occur are stronger candidates than routine narrative reports.
4. Consider schema additions only when repeated assessments show that referenced context cannot be expressed or validated adequately.

These priorities preserve the independent STAMPED runtime while allowing evidence from different vendors and collectors to inform its development.
