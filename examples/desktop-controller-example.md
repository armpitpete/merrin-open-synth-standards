# Example — Desktop Controller

This example shows how a desktop or angled performance controller can apply SLS-1 v3 and HIL-1.

It is illustrative, not human-recognition evidence.

## Device

```text
Example name: Two-Hand Harmonic/Event Controller
Format: angled desktop controller
Main functions: left-hand rhythm/events, right-hand pitch/harmony, rear CV/MIDI outputs
```

## HIL-1 layout principle

For a desktop controller, the main surface belongs to the hands.

```text
player side
↓
main hand/performance surface
↓
secondary controls
↓
rear/lower rear patch edge
```

## SLS-1 v3 state map

| Behaviour | State | Expression |
|---|---|---|
| Controller ready | IDLE | white dim steady |
| Performance surface active | ACTIVE | green steady |
| Shift/alternate layer | ALT / SHIFTED | blue steady |
| Output muted | MUTED / BYPASSED | white slow flash |
| Calibration armed | ARMED | amber steady at labelled calibration control |
| Confirm calibration save | CONFIRM REQUIRED | amber slow flash at labelled confirm control |
| Writing calibration | RECORD / WRITE | red steady at labelled write control |
| External clock lost | CLOCK LOST | blue slow flash at CLOCK label |
| Non-fatal degraded state | WARNING | amber fast flash + warning carrier |
| Fault / unsafe state | ERROR | red fast flash + error carrier |

## Placement

Use local lights for local functions. Do not make one anonymous light carry calibration, clock, write, warning, and error by memorised pulse words.

Critical states require contextual reinforcement through label, position, text, symbol, or a dedicated indicator.

## Common mistake

Weak design:

```text
A single light uses several counted rhythms for every controller state.
```

Better design:

```text
Use simple colour/motion and put the indicator where its meaning is obvious.
```
