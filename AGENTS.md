# Working on STAMPED assessments

Keep runtime, validation, and contribution workflows independent of Skills Workshop.
The canonical record model is LinkML under `src/stamped_assessment/data/schemas/`.
After model changes, run `pixi run generate` and review the generated schemas.
Run `pixi run test` and `pixi run validate` for affected implementation or record changes.
Preserve original assessments and separate review assertions; never label agent review as human review.
Keep source versions and checksums pinned and distinguish schema versions from instance versions.
