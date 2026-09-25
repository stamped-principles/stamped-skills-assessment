# Develop the assessment tools

```sh
pixi install --locked
pixi run generate
pixi run test
pixi run validate
pixi run python -m build
```

LinkML is a development dependency; the runtime uses generated JSON Schema plus semantic checks.
Change the LinkML source, regenerate all five record schemas, and review the diff.
Source updates require deliberate replacement of the vendored upstream files and their version/checksum lock.
The offline loader verifies checksums and reference-version compatibility on every validation.
A future schema release must retain validation support for older records or provide an explicit migration.
Version 0.1 currently accepts only its own model and reference bundle.

Tests exercise evidence requirements, incomplete scope, blocked access, stale reviews, references, duplicate identities, cyclic composition, and review prioritization.
They do not establish assessor reliability.
The inspection pilot is unreviewed observational material; it is not a controlled evaluation.
