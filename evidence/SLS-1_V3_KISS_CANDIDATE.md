# SLS-1 v3 KISS candidate evidence

## Decision

The v2 72-trial Morse-like recognition gate is superseded before Proofkeeper review.

Reason: the design required users to distinguish counted and ordered pulse signatures. The v3 candidate applies KISS instead of spending evidence effort proving that complexity can be learned.

## v3 design change

- Colour carries category.
- Motion is limited to steady, slow flash, fast flash.
- Context carries exact local meaning.
- Counted pulses, short/long signatures, and breathing codes are forbidden.
- A single unlabelled global indicator is deliberately limited to IDLE / ACTIVE / WARNING / ERROR.
- Exact critical states require a second carrier such as label, position, text, symbol, or dedicated indicator.

## First v3 human gate — FAIL

Exact candidate: `38f1cf529e35a9eac38181e5f22000572b44dc0a`

First completed unfamiliar-person run:

- 17/21 correct — 81.0%;
- IDLE 3/3;
- ACTIVE 3/3;
- ARMED 3/3;
- CONFIRM REQUIRED 1/3;
- RECORD / WRITE 1/3;
- WARNING 3/3;
- ERROR 3/3;
- one prohibited RECORD / WRITE ↔ ERROR confusion.

Verdict: **FAIL**.

Interpretation: broad status categories were recognised, but the blind anonymous-light presentation did not reliably communicate exact action states.

This does not justify adding more pulse words. The blind harness had removed the contextual carrier that v3 itself requires for exact critical meanings.

The raw first-run JSON is preserved in the PR #9 discussion and remains immutable evidence for `38f1cf52…`.

## Corrective human gate

The correction tests the complete intended presentation:

```text
SYSTEM: STATUS | WARNING | ERROR
ACTION: ARM | CONFIRM | WRITE
```

The labelled position is part of the signal.

The corrective gate keeps:

- seven core states;
- three repetitions each: 21 trials;
- at most 20 seconds of legend exposure;
- exactly one second of observation;
- the same >=90% overall threshold;
- perfect ERROR / CONFIRM REQUIRED / RECORD WRITE requirements;
- the same prohibited-confusion checks.

A new exact candidate requires a **different unfamiliar tester**. The earlier tester is no longer eligible because they have completed a v3 recognition run.

## Evidence boundary

Repository tests can verify the KISS vocabulary, fixed context map, and harness mechanics. They cannot supply the unfamiliar human-recognition evidence.

Proofkeeper remains blocked until the corrected human gate passes.
