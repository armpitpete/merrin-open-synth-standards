# Example — Desktop Controller

This example shows how a desktop or angled performance controller can apply SLS-1 v2 and HIL-1.

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

## Suggested physical layout

```text
REAR EDGE / PATCH EDGE
CV OUTS | GATE OUTS | CLOCK | MIDI | USB | POWER

SECONDARY CONTROLS
mode, scale, range, calibration, panic

MAIN PERFORMANCE SURFACE
[left hand: timing/events]     [right hand: pitch/harmony]

PLAYER SIDE
```

## HIL-1 notes

- Patch cables leave from the rear edge.
- No cable crosses the main hand surface.
- Large performance controls are central.
- Service/calibration controls stay away from the performance surface.
- Panic/stop remains reachable.
- Left-hand and right-hand roles are visually clear.

## SLS-1 v2 state map

| Behaviour | SLS-1 state | Pattern |
|---|---|---|
| Controller powered and ready | IDLE | P0 `STEADY_DIM` |
| Performance surface active | ACTIVE | P1 `STEADY_MID` |
| Shift/alternate layer held | ALT / SHIFTED | P2 `BREATHE_SLOW` |
| Output muted | MUTED / BYPASSED | P3 `PULSE_LONG_1HZ` |
| Calibration armed | ARMED | P5 `DOUBLE_EQUAL_1HZ` |
| Confirm calibration save | CONFIRM REQUIRED | P6 `TRIPLE_EQUAL_1HZ` |
| Writing calibration | RECORD / WRITE | P4 `PULSE_SHORT_1HZ` |
| External clock lost | CLOCK LOST | P9 `CLOCK_LOST_WIDE_DOUBLE` |
| Non-fatal degraded state | WARNING | P7 `WARNING_SHORT_LONG` |
| Fault or unsafe state | ERROR | P8 `ERROR_LONG_SHORT` |

## LED placement

Use local lights for local functions.

```text
- left-hand event state light near left-hand event surface
- right-hand harmony state light near right-hand harmony surface
- global error/status light near title or system area
- calibration/confirm light near calibration/save control
```

Do not hide armed, confirm, warning, clock-lost, or error lights in decorative lighting.

## Compliance notes

```text
HIL-1:
- Main performance surface clear of cables: design intent
- Patching placed at rear/lower edge: design intent
- Panic/stop accessible: design intent

SLS-1:
- Critical global signatures are distinct in the v2 contract: yes
- Calibration write uses arm/confirm/write states: yes
- Clock lost has its own global pattern: yes
- Human recognition test: not performed in this illustrative example
```

## Common mistake

Weak design:

```text
CV jacks placed across the centre because there was empty space.
```

Better design:

```text
Keep the centre playable. Put patching at the rear, lower rear, or side edge.
```
