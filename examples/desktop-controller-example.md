# Example — Desktop Controller

This example shows how a desktop or angled performance controller can apply SLS-1 and HIL-1.

It is illustrative, not mandatory.

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

## SLS-1 state map

| Behaviour | SLS-1 state | Pattern |
|---|---|---|
| Controller powered and ready | IDLE | STEADY_DIM |
| Performance surface active | ACTIVE | STEADY_MID |
| Shift/alternate layer held | ALT / SHIFTED | BREATHE_SLOW |
| Output muted | MUTED / BYPASSED | PULSE_0p5HZ |
| Calibration armed | ARMED | DOUBLE_PULSE_WIDE |
| Confirm calibration save | CONFIRM REQUIRED | TRIPLE_PULSE_WIDE |
| Writing calibration | RECORD / WRITE | PULSE_1HZ |
| External clock lost | CLOCK LOST | PULSE_0p5HZ or documented clock-lost pattern |
| Fault or unsafe state | ERROR | STEADY_BRIGHT |

## LED placement

Use local lights for local functions.

```text
- left-hand event state light near left-hand event surface
- right-hand harmony state light near right-hand harmony surface
- global error/status light near title or system area
- calibration/confirm light near calibration/save control
```

Do not hide armed, confirm, or error lights in decorative lighting.

## Compliance notes

```text
HIL-1:
- Main performance surface clear of cables: yes
- Patching placed at rear/lower edge: yes
- Diagnostics separated: yes
- Panic/stop accessible: yes
- Left/right hand roles readable: yes

SLS-1:
- State patterns documented: yes
- Calibration write uses arm/confirm/write states: yes
- Clock lost distinct from normal activity: yes
- No strobe or random flicker: yes
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
