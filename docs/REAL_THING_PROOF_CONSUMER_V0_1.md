# Real-Thing Proof consumer v0.1

Merrin Open Synth Standards consumes the canonical Real-Thing Proof / Project Status v2 controls without turning repository publication into evidence that a standard is mature in real use.

## Exact authorities

- Threadkeeper: `armpitpete/threadkeeper@a5bc55336c86097301b378d8654ac92a26ef81e5`
- Project Status v2: `armpitpete/merrin-project-controls@7bc8b7f5ef921851ad163093f089d28d8128bf6c`
- Canonical validator snapshot: `vendor/merrin-project-controls/7bc8b7f5ef921851ad163093f089d28d8128bf6c/validate_project_status.py`
- Canonical validator Git blob: `d0e704ab42d72da6b66fb1d9f31d739ed6220abd`
- Repository lifecycle record: `project-status.json`

The repository lifecycle record and the maturity status of an individual standard answer different questions.

## Repository lifecycle

`project-status.json` records the bounded standards-governance foundation accepted at baseline `1ff86360b4b715d35e4b9dd0e0e7d69651435461`.

That foundation has direct evidence through merge for its actual contract: proposal/evidence/review/versioning/publication governance. It has no separate runtime deployment or live-behaviour surface, and repository-level human acceptance is not required merely to prove that the governance foundation was reviewed and merged.

Those `NOT_APPLICABLE` stages do **not** waive evidence required by an individual standard.

## Standard maturity

The standard-status vocabulary remains:

- `Draft` — provisional and not yet proven sufficiently;
- `Freeze Candidate` — believed coherent and ready for bounded real use, supported by bounded implementation or use evidence and review appropriate to that status;
- `Stable` — used successfully across multiple independent instrument or implementation contexts;
- `Deprecated` — explicitly retired or replaced.

A Git commit, pull-request merge, release note, repository publication, CI pass or documentation review cannot by itself promote a standard to `Freeze Candidate` or `Stable`.

Likewise, a standard may be `Stable` while some unrelated repository lifecycle action is unfinished. Maturity and repository lifecycle are separate evidence dimensions.

## Evidence sidecars for future promotion

Current HIL-1 and SLS-1 remain `Draft`; this lane does not change either standard.

Future non-Draft maturity claims use a companion JSON record at:

`evidence/maturity/<standard_id>.json`

The repository validator checks only what can be checked mechanically. Human review still has to judge whether evidence genuinely exercises the claimed environment.

### Freeze Candidate

A companion record must identify:

- the exact `standard_id` and `status`;
- at least one bounded implementation or use evidence item;
- an evidence-backed review decision accepting the current status.

A Freeze Candidate can still be awaiting broader or player-facing real use. The required evidence shows that the proposal has moved beyond documentation-only assertion; it does not convert the candidate into `Stable`.

### Stable

A companion record must identify:

- the exact `standard_id` and `status`;
- at least two distinct implementation contexts;
- an evidence pointer for each implementation;
- an explicit declaration that each item is intended as an independent implementation context;
- an evidence-backed review decision accepting `Stable`.

The mechanical declaration is not proof of independence by itself. Review must reject duplicated, derivative or proxy contexts that do not satisfy the actual claim.

### Deprecated

A companion record must identify the reason for deprecation and an evidence-backed review decision. A replacement may be named where one exists.

## Public summary consistency

Where `README.md` publishes a standard's maturity status, that status must match the standard's frontmatter. This prevents the public summary from silently claiming a higher maturity state than the authoritative standard file.

## Human, accessibility and safety claims

Documentation can define accessibility, safety and player-facing requirements. It cannot prove those requirements work in a real instrument or interface.

Where a maturity claim relies on playability, physical layout, sensory safety, accessibility or real-world comprehension, the evidence must come from the relevant real implementation or human surface. CI and repository review remain supporting evidence only.

## Current boundary

Both current standards remain `Draft`. No `Freeze Candidate`, `Stable`, universal-adoption, physical-proof, accessibility-acceptance, safety-acceptance or player-acceptance claim is created by this adoption lane.
