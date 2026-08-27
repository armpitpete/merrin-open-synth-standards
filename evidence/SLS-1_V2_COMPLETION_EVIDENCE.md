# SLS-1 v2.0 completion evidence

Issue: #7

Baseline:

```text
repository: armpitpete/merrin-open-synth-standards
main: 1ff86360b4b715d35e4b9dd0e0e7d69651435461
```

## Claim discipline

This record separates what has been mechanically demonstrated from what still requires a human or real instrument.

### Direct mechanical evidence

The candidate includes:

- normative machine-readable pattern data;
- a validator for timing, rolling-window pulse ceiling, required mappings, critical cyclic uniqueness and reduced-motion fallback structure;
- regression tests that deliberately break those invariants;
- an executable browser reference resolver/renderer;
- Node tests for resolver precedence and reduced-motion state preservation.

Local pre-commit execution performed during preparation:

```text
python scripts/validate_sls1.py
PASS

python -m unittest discover -s tests -v
6 tests PASS

node tests/test_sls_reference.mjs
PASS
```

These results demonstrate the local candidate logic that was prepared for the branch. The authoritative repository result is the exact-head CI result after the files are committed.

### Design correction evidence

The v2 contract removes the known v1 structural defects:

- no critical global cyclic pattern exceeds a one-second cycle;
- WARNING has a canonical pattern;
- ERROR has a temporal pattern rather than brightness-only distinction;
- critical global states have distinct cyclic signatures;
- CLOCK LOST no longer shares the MUTED pattern on a global indicator;
- reduced-motion fallbacks exist for all critical global states.

### External design context

SLS-1 is intentionally narrower than general standards. IEC 60073 provides general coding principles for indicators and actuators. W3C/WCAG provides flashing and motion-related accessibility requirements for web/software surfaces.

SLS-1's `≤3 visible on-pulses per rolling second` rule is an internal conservative design invariant and must not be described as automatic proof of every external flash threshold.

## Not yet direct evidence

The following must **not** be marked PASS from repository checks alone:

- human one-second recognition;
- player acceptance;
- physical LED viewing-distance performance;
- ambient-light performance;
- mis-press safety on a real destructive operation;
- crash/brownout behaviour on physical hardware;
- multi-implementation adoption.

## Current maturity decision

**Remain `Draft`.**

Reason:

The candidate is mechanically coherent and executable, but SLS-1 itself requires human recognition evidence for a conforming implementation. That evidence has not yet been collected.

The next maturity decision may consider `Freeze Candidate` only after:

1. exact-head CI passes;
2. independent exact-head review accepts the candidate;
3. at least one bounded implementation completes the random-phase human recognition protocol without the prohibited confusions;
4. the evidence record is updated without converting unperformed checks into PASS.

`Stable` remains out of scope until successful use exists across multiple implementation contexts.
