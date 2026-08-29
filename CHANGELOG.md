# Changelog

All notable changes to Merrin Open Synth Standards are recorded here.

The format is plain and project-facing rather than strict semantic versioning.

## 2026-08-29 — SLS-1 v3.0-draft KISS candidate

### Decision

The v2 72-trial recognition gate was stopped before independent Proofkeeper review.

The reason was architectural rather than evidential: v2 required a user to distinguish a Morse-like vocabulary of double/triple and ordered short/long pulse signatures. SLS-1 v3 applies KISS instead of proving that complexity can be memorised.

### Changed

- Colour now carries the broad semantic category.
- Temporal encoding is limited to exactly three behaviours: steady, slow flash, fast flash.
- Exact local meaning comes from context: label, position, text, symbol, or a dedicated indicator.
- A single unlabelled global indicator is limited to IDLE / ACTIVE / WARNING / ERROR.
- Critical exact meanings require a non-colour secondary carrier.
- Counted pulse groups, short–long/long–short signatures, breathing codes, random flicker, and decorative state animation are forbidden.
- The human gate is reduced from 72 trials to 21: seven core states × three repetitions.
- The new gate requires an unfamiliar tester and at most 20 seconds of legend exposure.

### Evidence boundary

Mechanical validation can prove contract consistency and harness behaviour.

It cannot supply the unfamiliar-person recognition result, physical LED evidence, ambient-light evidence, or player acceptance.

Proofkeeper review remains blocked until the unfamiliar-person recognition gate passes.

## 2026-08-27 — SLS-1 v2.0-draft completion candidate

v2 introduced executable conformance and repaired multiple timing/precedence defects, but its recognition architecture was superseded by the v3 KISS decision before review/merge.

## 2026-07-11 — Initial public standards set

### Added

- Added repository README.
- Added CC BY 4.0 licence notice.
- Added attribution notice.
- Added `MERRIN-STD-SLS-1 — State Lantern System`.
- Added `MERRIN-STD-HIL-1 — Human Interface Layout`.

### Status

Both standards are published as drafts.
