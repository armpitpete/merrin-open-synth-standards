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

## Human gate

The replacement human-recognition gate uses seven core states, three repetitions each: 21 trials.

The tester must be unfamiliar with SLS-1 v3, may read the tiny legend for at most 20 seconds, then gets one second per trial.

The first completed run is evidence. No practice/restart/repeat for score improvement.

Proofkeeper remains blocked until this human gate passes.

## Evidence boundary

Repository tests can verify the KISS vocabulary and harness mechanics. They cannot supply the unfamiliar human-recognition evidence.
