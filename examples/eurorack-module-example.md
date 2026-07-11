# Example — Eurorack Module

This example shows how a small Eurorack-style module can apply SLS-1 and HIL-1.

It is illustrative, not mandatory.

## Module

```text
Example name: Small Delay / Memory Module
Width: 8HP or 10HP
Main functions: input, delay/memory, feedback, wet/dry output
```

## HIL-1 layout

Use Pattern A unless a documented exception is needed.

```text
Title / identity
↓
main performance controls
↓
secondary controls and mode switch
↓
state LEDs near affected controls
↓
patch jacks
```

## Suggested panel order

```text
[ Module name ]

[ Time ]     [ Feedback ]
[ Mix  ]     [ Tone     ]

[ Mode button ]  [ State LED ]

IN     CV TIME     CV FB
OUT    CLOCK       RESET
```

## HIL-1 notes

- Main knobs are above the patch cable area.
- Patch jacks are grouped at the bottom.
- The state LED is next to the mode button because it describes that control’s state.
- Feedback is a risky control, so it should not be tiny or hidden.
- If feedback can self-oscillate hard, add clear marking and consider a warning state.

## SLS-1 state map

| Behaviour | SLS-1 state | Pattern |
|---|---|---|
| Powered but idle | IDLE | STEADY_DIM |
| Delay active | ACTIVE | STEADY_MID |
| Alternate mode held | ALT / SHIFTED | BREATHE_SLOW |
| Delay path bypassed | MUTED / BYPASSED | PULSE_0p5HZ |
| About to clear memory | ARMED | DOUBLE_PULSE_WIDE |
| Waiting for confirm clear | CONFIRM REQUIRED | TRIPLE_PULSE_WIDE |
| Writing/saving setting | RECORD / WRITE | PULSE_1HZ |
| Feedback unsafe/high | WARNING | documented distinct warning pattern |
| Internal fault | ERROR | STEADY_BRIGHT |

## Compliance notes

```text
HIL-1:
- Main controls reachable when patched: yes
- Jacks grouped at bottom: yes
- State LED near affected function: yes
- Dangerous action protected: yes, clear-memory requires arm/confirm

SLS-1:
- State patterns documented: yes
- No pattern exceeds 3 pulses/sec: yes
- Colour not required as the only signal: yes
- Error and confirm are distinct: yes
```

## Common mistake

Weak design:

```text
LED blinks randomly with delay activity and also means armed/error.
```

Better design:

```text
Audio activity has its own meter or is omitted.
State LED follows SLS-1 state precedence.
```
