# Example — Eurorack Module

This example shows how a small Eurorack-style module can apply SLS-1 v2 and HIL-1.

It is illustrative, not human-recognition evidence.

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

## SLS-1 v2 state map

| Behaviour | SLS-1 state | Pattern |
|---|---|---|
| Powered but idle | IDLE | P0 `STEADY_DIM` |
| Delay active | ACTIVE | P1 `STEADY_MID` |
| Alternate mode held | ALT / SHIFTED | P2 `BREATHE_SLOW` |
| Delay path bypassed | MUTED / BYPASSED | P3 `PULSE_LONG_1HZ` |
| About to clear memory | ARMED | P5 `DOUBLE_EQUAL_1HZ` |
| Waiting for confirm clear | CONFIRM REQUIRED | P6 `TRIPLE_EQUAL_1HZ` |
| Writing/saving setting | RECORD / WRITE | P4 `PULSE_SHORT_1HZ` |
| Feedback unsafe/high | WARNING | P7 `WARNING_SHORT_LONG` |
| Internal fault | ERROR | P8 `ERROR_LONG_SHORT` |

## Clear-memory flow

```text
normal
→ deliberate clear/arm
→ ARMED
→ deliberate proceed
→ CONFIRM REQUIRED
→ confirm inside documented window
→ RECORD / WRITE while memory is actually cleared
→ IDLE/ACTIVE on success
→ WARNING/ERROR on failure
```

Timeout or cancel must not clear memory.

## Compliance notes

```text
HIL-1:
- Main controls reachable when patched: design intent
- Jacks grouped at bottom: design intent
- State LED near affected function: design intent

SLS-1:
- State patterns documented: yes
- Critical patterns come from v2 machine contract: yes
- Colour is not required as the only carrier: yes
- Human recognition test: not performed in this illustrative example
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
