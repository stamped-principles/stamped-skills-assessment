# Assessment design, version 0.1

## Purpose and priorities

STAMPED provides a vocabulary for reasoning about an object's properties.
A rubric states what matters for a specific objective, why it matters, and what evidence would demonstrate the desired state.
Each of the seven principles receives a priority and a direction: maximize, balance, or preserve.
These are use-case decisions, not amendments to the normative principles.
A low-priority criterion can still represent an unmet normative requirement.
An excluded principle needs an explicit rationale.

Ephemerality must name the component to which it applies.
A disposable build environment can serve a permanently preserved manuscript.
Treating the manuscript itself as disposable would serve a different objective.
Future rubric refinements should support more precise component-specific targets where the pilot demonstrates the need.

## Comprehensiveness, resources, and conclusions

The rubric declares required evidence-gathering activities for each criterion.
The assessment plan can add activities, but cannot silently omit those requirements.
Activities are named capabilities, not a universal ladder of agent effort.
Inspection, reference resolution, retrieval, environment construction, execution, comparison, and independent reproduction can each expose different evidence.
An efficient assessor may perform comprehensive work with little compute.

Conditions describe available assistance, permitted actions, access context, resource limits, and environment.
They do not grant permission to create accounts, accept terms, acquire restricted data, spend money, or publish.
Observations record completed, blocked, or unattempted activities.
Blocked work records the barrier, a possible next action, and whether user help is needed.
An unattempted activity must not be mislabeled as a discovered access barrier.

`finalized` means the assessor has issued a report accounting for its plan.
It does not mean reproduction succeeded or all planned activities were completed.
The CLI derives `scope_accounted_for` and `scope_completed` separately.
Completion of an activity can yield a negative or inconclusive judgment.
A positive judgment requires evidence from every activity required by its rubric criterion.

Neither restricted access nor a missing account alone proves a universal Distributability failure.
Record the intended recipient, known retrieval conditions, and what this assessor could establish.
Likewise, successful reproduction is evidence about that procedure under those conditions, not proof of all STAMPED principles or scientific correctness.

## Criteria, evidence, and comparison

Rubrics reference stable checklist item identifiers from an exact locked reference bundle.
They may include additional criteria with no checklist mapping.
The tool checks known identifiers and matching categories but does not claim the criterion exhaustively represents its linked checklist item.
No full-checklist coverage or whole-object compliance is inferred from selected criteria.

Evidence is a locator and description, optionally with a content digest.
Inspecting a command definition is different from observing it execute.
Evidence identifiers in judgments must refer to observations of the same criterion.
Structural validation cannot decide whether a human or agent's judgment follows logically from the evidence.
That remains a review task.

Summaries preserve per-principle counts, priorities, and unknowns.
There is no overall score or implied equal weighting of principles.
Comparisons are meaningful only when object versions, rubric identity, source versions, task, conditions, and assessor instrument are known.
`comparison_group` links related records without claiming a controlled experiment.
Assessing whether a skill helped will require matched tasks and conditions, explicit interventions, and repeated independent evaluations.

## Review at increasing scale

Reviews refer to an exact semantic record digest, so reformatting YAML does not invalidate them while changing a judgment does.
They preserve the original assertion and can propose a different status.
Human and agent reviewers remain distinguishable; a YAML identity is an assertion, not authenticated proof.
Maintainer review of Git contributions provides the initial publication trust boundary.
Corrections use new records and `supersedes`, preserving earlier history.

The initial queue prioritizes explicit disagreements, different judgments on the same object and rubric, and unresolved criteria marked essential.
It also requests initial human calibration for every new rubric criterion and retains deterministic sampling after calibration.
Reasons appear alongside priority so reviewers can challenge the policy.
These priorities are a provisional review policy, not a scientific quality score.
Automated agreement does not silently become human approval.

SHACL Vue is a promising form editor for schema-derived review records.
Orinoco's implementation also needs RDF/SHACL resources, application-specific editor packaging, and a separately authenticated GitHub handoff.
A schema alone does not supply that application.
This prototype keeps review decisions in portable records and a CLI queue, providing a future editor with stable record and criterion identifiers.
The next UI experiment should verify LinkML-to-SHACL generation and round-trip preservation of nested observations and separate reviews before adopting that stack.
No hosted service or UI is part of this first version.

## Organization and distribution

The assessment repository owns the model, validator, reference data, rubrics, and record store.
The agent-skills repository owns the installable assessor instructions and their agent adapters.
APM owns skill installation and integrity; Python packaging owns executable assessment tooling.
Consumers can use the CLI and contribute records without installing a skill, and the skill has no Workshop dependency.

Sources informing this design:

- https://github.com/stamped-principles/stamped-agent-skills/issues/2
- https://github.com/bids-standard/bids-specification/tree/master/tools/schemacode
- https://github.com/con/skills/pull/13#pullrequestreview-5321975771
- https://github.com/ORINOCO-Lite/orinoco-lite-dev

The APM review favors using the actual package manager and avoiding duplicated discovery logic.
It also argues for separating content changes from directory moves; historical drafts remain distinguishable from the new assessor.
