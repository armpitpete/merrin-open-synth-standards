# Changelog

All notable changes to Merrin Open Synth Standards are recorded here.

The format is plain and project-facing rather than strict semantic versioning.

## 2026-08-29 — SLS-1 v3.0-draft KISS candidate

### Decision

The v2 72-trial recognition gate was stopped before independent Proofkeeper review.

The reason was architectural rather than evidential: v2 required a user to distinguish a Morse-like vocabulary of double/triple and ordered short/long pulse signatures. SLS-1 v3 applies KISS instead of proving that complexity can be memorised.

### Changed

- Colour carries broad semantic category.
- Temporal encoding is limited to exactly three behaviours: steady, slow flash, fast flash.
- Exact local meaning comes from context: label, position, text, symbol, or a dedicated indicator.
- A single unlabelled global indicator is limited to IDLE / ACTIVE / WARNING / ERROR.
- Critical exact meanings require a non-colour secondary carrier.
- Counted pulse groups, short–long/long–short signatures, breathing codes, random flicker, and decorative state animation are forbidden.
- Product documentation must define the colour categories, motion categories, critical meanings, and local labels/symbols.

### Human-use model

SLS-1 now explicitly models ordinary indicator learning:

```text
notice
→ investigate
→ lookup
→ learned recognition
```

An unfamiliar person is **not** required to infer an exact state name on first sight.

### Browser recognition research

Two unfamiliar-person browser protocols were tried during v3 design.

1. Blind single-light candidate `38f1cf529e35a9eac38181e5f22000572b44dc0a`: 17/21 (81.0%), FAIL. Exact action states were the main weakness because the test removed the contextual carrier.
2. Labelled-panel candidate `e3347fa4182ab168f53e858be75fb81bb33cce45`: 14/21 (66.7%), FAIL. The complete six-position panel was shown for one second and hidden before answer, turning the task partly into visual search and short-term recall.

Both failures remain valid negative evidence for those protocols. They do not justify more blink codes.

### Corrective acceptance model

Abstract browser exact-naming quizzes are no longer SLS-1 conformance gates.

Human evidence belongs with realistic implementations and asks whether important states are noticed, whether the user can find and understand the explanation, and whether ordinary reuse increases familiarity.

### Evidence boundary

Mechanical validation can prove the bounded colour/motion vocabulary, critical-state context requirements, documentation requirements, and declared human-use model.

It cannot prove real-world noticeability, physical LED performance, ambient-light performance, accessibility for every user, learning retention, or player acceptance.

Independent review may evaluate the draft specification inside those stated boundaries. Physical and longitudinal evidence belongs to later implementation maturity.

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
