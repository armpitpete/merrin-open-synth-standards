# SLS-1 v1.0-draft → v2.0-draft migration

## Classification

**Breaking draft revision.**

SLS-1 keeps the identifier `MERRIN-STD-SLS-1`, but v2.0 changes normative pattern timing and default mappings. A v1.0 implementation must not claim v2.0 conformance without retesting.

The published v1.0-draft remains recoverable at repository commit:

```text
11ecdeb3f2c27db09d065e3bca69746a3d83b7c9
```

and is also present in the repository history leading to baseline:

```text
1ff86360b4b715d35e4b9dd0e0e7d69651435461
```

## Why the major version changed

v1.0 contained three material defects:

1. some critical patterns used two-second cycles despite a one-second recognition target;
2. ERROR defaulted to steady bright, making its distinction from ordinary steady ACTIVE depend heavily on brightness;
3. WARNING had no canonical pattern and therefore allowed the private per-instrument vocabulary SLS-1 was intended to prevent.

v2.0 also makes global-versus-local uniqueness explicit and adds reduced-motion equivalence for software surfaces.

## Pattern migration

| State | v1.0 default | v2.0 default |
|---|---|---|
| IDLE | `STEADY_DIM` | `P0 STEADY_DIM` |
| ACTIVE | `STEADY_MID` | `P1 STEADY_MID` |
| ALT / SHIFTED | `BREATHE_SLOW` | `P2 BREATHE_SLOW` |
| MUTED / BYPASSED | `PULSE_0p5HZ` | `P3 PULSE_LONG_1HZ` |
| RECORD / WRITE | `PULSE_1HZ` | `P4 PULSE_SHORT_1HZ` |
| ARMED | `DOUBLE_PULSE_WIDE` / 2 s | `P5 DOUBLE_EQUAL_1HZ` / 1 s |
| CONFIRM REQUIRED | `TRIPLE_PULSE_WIDE` / 2 s | `P6 TRIPLE_EQUAL_1HZ` / 1 s |
| WARNING | implementation-defined | `P7 WARNING_SHORT_LONG` |
| ERROR | `STEADY_BRIGHT` | `P8 ERROR_LONG_SHORT` |
| CLOCK LOST | often shared with MUTED | `P9 CLOCK_LOST_WIDE_DOUBLE` for global use |

## Required implementation changes

### Physical LED implementation

- replace v1 timing constants with the v2 machine contract;
- make WARNING and ERROR temporal on a global status LED;
- give CLOCK LOST its own global signature;
- retest from random pattern phase;
- confirm no rolling one-second interval exceeds three visible on-pulses.

### Software implementation

Do the physical/state changes above, plus:

- retain text/symbol state in addition to colour;
- honour reduced-motion preference with a static equivalent for critical animated states;
- keep resolver precedence unchanged by rendering mode.

## State-machine changes

For staged destructive/high-impact actions:

```text
safe → ARMED → CONFIRM REQUIRED → RECORD / WRITE → safe
                                      ↘ WARNING / ERROR on failure
```

Timeout or cancel from ARMED/CONFIRM REQUIRED must return to a safe non-writing state and must never execute the action.

## Retest checklist

- [ ] machine validator passes;
- [ ] resolver precedence passes;
- [ ] random-phase one-second human recognition performed;
- [ ] ARMED/WARNING confusion = zero;
- [ ] ERROR/ACTIVE confusion = zero;
- [ ] destructive mis-press test passes;
- [ ] crash/reset fail-safe passes;
- [ ] reduced-motion equivalence passes where applicable;
- [ ] implementation conformance record updated to v2.0.
