# Changelog

All notable changes to Merrin Open Synth Standards are recorded here.

The format is plain and project-facing rather than strict semantic versioning.

## 2026-08-27 — SLS-1 v2.0-draft completion candidate

### Changed

- Reworked SLS-1 critical timing so every critical global pattern has a complete cycle of one second or less.
- Added canonical WARNING and ERROR rhythms.
- Separated CLOCK LOST from MUTED/BYPASSED on global indicators.
- Defined global-versus-local pattern uniqueness.
- Defined staged `ARMED → CONFIRM REQUIRED → RECORD / WRITE` behaviour including cancel/timeout/failure rules.
- Added reduced-motion equivalents for software critical states.
- Added an explicit breaking-change migration record from v1.0-draft.

### Added

- Machine-readable SLS-1 v2 pattern contract.
- Mechanical pattern validator and regression tests.
- Browser reference resolver/renderer and Node regression test.
- SLS-1-specific GitHub Actions validation workflow.
- Evidence record separating mechanical proof from human/player evidence.

### Status

SLS-1 remains `Draft`.

The candidate does not claim human one-second recognition, physical acceptance, or multi-implementation adoption from repository tests alone.

## 2026-07-11 — Initial public standards set

### Added

- Added repository README.
- Added CC BY 4.0 licence notice.
- Added attribution notice.
- Added `MERRIN-STD-SLS-1 — State Lantern System`.
- Added `MERRIN-STD-HIL-1 — Human Interface Layout`.

### Status

Both standards are published as drafts.

### Notes

- SLS-1 and HIL-1 are deliberately separate.
- SLS-1 answers: `What does this light mean?`
- HIL-1 answers: `Where should this control, jack, LED, or performance area go?`
- The repo is not claiming universal authority. These are practical working standards published for reuse, critique, and adaptation.
