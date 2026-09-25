# Contribute an assessment

Choose or create a use case and a rubric before assessing an object.
State whose objective the rubric represents and whether its priorities were chosen by the user, assessor, or jointly.
Identify exact source versions or hashes and the object boundary, including essential components.
Do not use a mutable branch name as a snapshot identity.

Create YAML records under `records/<record_type>/` with globally unique IDs.
Treat published records as immutable: changed use cases, objects, or rubrics receive new IDs, and assessment or review corrections use new records with `supersedes` where applicable.
Use the existing pilot as a concrete shape example, not as a universal rubric.
Export a record schema with `stamped-assess schema assessment` or another record type.
Read the model's descriptions for nested fields.
Store substantial evidence at stable locations and retain references; omit secrets and material that cannot be contributed publicly.

Declare permitted activities, assistance, access conditions, and resource limits.
Record every planned activity as completed, blocked, or not attempted.
A finalized report needs every criterion judgment and seven principle summaries, even when some findings remain unknown.
Do not invent execution evidence or treat absent evidence as a demonstrated failure.

```sh
stamped-assess validate records
stamped-assess summarize records
stamped-assess review-queue records
stamped-assess review-report records --limit 10
stamped-assess digest records ASSESSMENT_ID
```

For review, create a separate `review` record with that digest and criterion-level decisions.
State the actual reviewer kind; agents must never record their own judgment as human review.
A reviewer can agree, disagree, or request more evidence and may suggest a corrected status.
A new review can supersede an earlier one while preserving both.
Only the same reviewer can supersede their own earlier review.
An amended assessment is a new record; earlier reviews continue to address the earlier assertion.
Assessment corrections retain object and rubric identity; use comparison_group when assessing another version or rubric.

Submit records and evidence changes through Git review.
Schema-valid means structurally accepted, not scientifically correct or human-approved.
Do not automatically post, push, or publish a contribution merely because an assessment was requested.
