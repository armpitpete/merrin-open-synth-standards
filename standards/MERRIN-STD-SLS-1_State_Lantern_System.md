---
standard_id: MERRIN-STD-SLS-1
title: State Lantern System
version: v1.0-draft
status: Draft
scope: State and mode LEDs/status lights for synth modules, browser synths, controllers, and performance instruments.
license: CC-BY-4.0
---

# MERRIN-STD-SLS-1 — State Lantern System

## 1. Purpose

SLS-1 defines a consistent, no-confusion light language for state LEDs and status lights.

It exists to stop every module or app inventing a private LED language.

In live use, a player should not have to guess whether a blinking light means:

- active
- muted
- armed
- recording
- waiting for confirmation
- warning
- error
- decorative activity

SLS-1 makes status readable quickly and safely.

## 2. Outcome

An SLS-1 compliant instrument should make states readable in one glance.

The system should ensure:

- states are readable in one second or less
- destructive actions are hard to trigger by accident
- risk states are never hidden
- rhythm carries meaning
- colour reinforces meaning but is not the only carrier
- state LEDs do not behave like decorative lights or meters

## 3. Scope

### Applies to

SLS-1 applies to any light that communicates:

- state
- mode
- arm/confirm flow
- record/write/save state
- mute/bypass state
- warning
- error
- transport or clock state
- safety condition

### Does not apply to

SLS-1 does not govern:

- purely decorative lighting
- audio meters
- clipping indicators
- signal-present indicators
- aesthetic animation that is clearly separate from state signalling

Activity indicators must not override or mask safety state indicators.

## 4. Core principles

1. **Light must mean something.** A state LED must not blink decoratively.
2. **Rhythm beats colour.** Assume single-colour LEDs first.
3. **Colour reinforces meaning.** Do not rely on colour alone.
4. **Readable in one second.** The important state must be recognisable fast.
5. **No hidden states.** If behaviour changes, the light must make that visible.
6. **Fail safe.** On crash, reset, or ambiguity, show IDLE or ERROR, never ARMED, CONFIRM, or WRITE.
7. **Small alphabet.** Reuse a short set of named patterns.
8. **Safety states override activity.** Pretty lights never outrank risk information.

## 5. Definitions

| Term | Meaning |
|---|---|
| State light | A light communicating behavioural state, not audio level. |
| Pulse | Light turns on, then returns off. One clear on-event. |
| Breathe | Smooth fade up/down with no hard blink edge. |
| Dim | Low steady brightness. |
| Mid | Normal readable brightness. |
| Bright | High warning/error brightness, not painful. |
| Decorative light | Light used for appearance only; must not be confused with state. |

## 6. Canonical states

### 6.1 Mandatory core states

| State | Meaning |
|---|---|
| IDLE | Default. Nothing engaged or waiting. |
| ACTIVE | Function/path/mode is engaged. |
| ALT / SHIFTED | Alternate layer is active. |
| MUTED / BYPASSED | Path/output intentionally suppressed. |
| ARMED | Risky or high-impact action staged, awaiting confirm. |
| CONFIRM REQUIRED | Explicitly requesting confirmation now. |
| RECORD / WRITE | Actively recording, writing, saving, or committing. |
| WARNING | Non-fatal issue; degraded behaviour possible. |
| ERROR | Fault requiring user action or blocking correct behaviour. |

### 6.2 Optional clock/transport states

Use only on clock-aware modules or apps.

| State | Meaning |
|---|---|
| CLOCK PRESENT | External clock detected and in use. |
| CLOCK LOST | Expected clock missing or invalid. |
| TRANSPORT RUN | Sequencer/transport running. |
| TRANSPORT STOP | Sequencer/transport stopped but ready. |

### 6.3 Optional focus states

| State | Meaning |
|---|---|
| SELECTED / FOCUSED | Channel, part, scene, or parameter is under edit. |
| LOCKED / HELD | A latched state persists until deliberately cleared. |

## 7. Pattern library

### 7.1 Hard sensory safety rule

No state pattern may exceed:

```text
3 visible pulses per second
```

measured as on-pulses in any rolling one-second window.

No strobe-like pattern is allowed.

### 7.2 Recommended timing

| Parameter | Recommendation |
|---|---|
| Pulse width | 120–200 ms on |
| Minimum pulse gap | 200 ms or more off |
| Breathe cycle | About 2 seconds |
| Signature time | Pattern identity readable within 1 second |

### 7.3 Canonical patterns

| Pattern ID | Name | Loop | Rhythm | Intended use |
|---|---|---:|---|---|
| P0 | STEADY_DIM | infinite | On at dim level | IDLE |
| P1 | STEADY_MID | infinite | On at mid level | ACTIVE |
| P2 | STEADY_BRIGHT | infinite | On at bright level | ERROR beacon |
| P3 | BREATHE_SLOW | 2s | Smooth fade up/down | ALT / SHIFTED or focus |
| P4 | PULSE_1HZ | 1s | One pulse each second | RECORD / WRITE |
| P5 | PULSE_0p5HZ | 2s | One pulse every two seconds | MUTED / BYPASSED or CLOCK LOST |
| P6 | DOUBLE_PULSE_WIDE | 2s | pulse, gap, pulse, rest | ARMED |
| P7 | TRIPLE_PULSE_WIDE | 2s | pulse, gap, pulse, gap, pulse, rest | CONFIRM REQUIRED |
| P8 | TICK_OVERLAY | 4s | one brief tick every four seconds | optional overlay or heartbeat |

## 8. Forbidden patterns

Non-compliant state patterns include:

- more than 3 pulses per second
- strobe or near-strobe blinking
- random flicker on a state LED
- meter-like animation on a state LED
- decorative blinking on a state LED
- warning and armed states that can be mistaken for each other
- colour-only state differences without rhythm/position/label support

## 9. State precedence

When multiple states are active, show the highest-precedence state.

Highest wins:

1. ERROR
2. CONFIRM REQUIRED
3. ARMED
4. RECORD / WRITE
5. WARNING
6. CLOCK LOST
7. MUTED / BYPASSED
8. ALT / SHIFTED
9. ACTIVE
10. IDLE

## 10. Tie-break rules

If multiple same-level states exist:

1. show the highest severity
2. if equal, show the most recent
3. if equal, prefer the selected/focused target
4. if still equal, use module-defined order and document it

## 11. Global vs local indicators

If an instrument has a global status light:

- the global light must show the highest-precedence state anywhere in the instrument
- local lights may show local states
- local lights must not contradict the global safety truth

Example:

```text
One channel is active.
Another channel is armed for overwrite.
Global state = ARMED.
Local channel lights may still show local detail.
```

## 12. Required state-to-pattern map

A compliant instrument must publish its local mapping.

Default map:

| Canonical state | Default pattern |
|---|---|
| IDLE | P0 |
| ACTIVE | P1 |
| ALT / SHIFTED | P3 |
| MUTED / BYPASSED | P5 |
| ARMED | P6 |
| CONFIRM REQUIRED | P7 |
| RECORD / WRITE | P4 |
| WARNING | distinct from ARMED and CONFIRM REQUIRED |
| ERROR | P2, optional P8 overlay |
| CLOCK LOST | P5 or another low-urgency distinct pattern |

WARNING must not be confusable with ARMED.

If WARNING uses a new pattern, document it clearly and keep it within the 3 pulses/sec safety rule.

## 13. Behaviour examples

| Behaviour | Canonical state |
|---|---|
| Shift held | ALT / SHIFTED |
| Channel muted | MUTED / BYPASSED |
| About to overwrite pattern | ARMED |
| Waiting for second press to commit | CONFIRM REQUIRED |
| Saving to flash/local storage | RECORD / WRITE |
| Missing SD card or missing required file | ERROR |
| External clock vanishes mid-run | CLOCK LOST |
| Mode active but safe | ACTIVE |

## 14. Implementation rules

### 14.1 Single resolver rule

Do not let LED patterns compete directly.

Use this flow:

```text
collect active states
↓
choose highest-precedence effective state
↓
render pattern for effective state
```

### 14.2 Boot/reset fail-safe

During boot, reset, or unknown state:

- show IDLE if the instrument is safe
- show ERROR if the instrument cannot verify safe state
- never show ARMED, CONFIRM REQUIRED, or RECORD / WRITE unless that state is true

### 14.3 Brightness

At minimum, provide readable dim/mid/bright levels.

Brightness should be:

- visible in low light
- not painful at close range
- consistent within one instrument

### 14.4 Activity separation

State lights must not animate like audio meters.

If an activity meter and a state light share a physical LED, safety state must take priority.

## 15. Accessibility rules

Do not make colour the only signal.

Use at least two of:

- rhythm
- label
- position
- shape/icon
- brightness
- screen text
- tactile grouping

Avoid rapid flashing, flicker, and ambiguous decorative effects.

## 16. Compliance tests

### Test 1 — one-second recognition

Goal: identify the displayed state in one second or less at normal playing distance.

Pass criteria:

- 90% or better recognition overall
- 100% recognition for ERROR, ARMED, CONFIRM REQUIRED, and RECORD / WRITE
- no ARMED/WARNING confusion

### Test 2 — mis-press safety

Goal: accidental destructive actions do not occur under distracted use.

Pass criteria:

- zero accidental destructive actions across 20 attempts
- ARMED and CONFIRM REQUIRED appear reliably during staged flows

### Test 3 — crash/reset fail-safe

Goal: LEDs do not lie during reset, hang, crash, or brownout.

Pass criteria:

- on fault, LEDs go to IDLE or ERROR
- LEDs never show ARMED, CONFIRM REQUIRED, or RECORD / WRITE unless true after recovery

### Test 4 — sensory safety

Goal: patterns remain safe and non-strobing.

Pass criteria:

- no pattern exceeds 3 pulses/sec
- no random flicker
- no strobe-like behaviour

## 17. Required conformance block

Each implementing project should include this block in its docs:

```text
SLS-1 conformance
Date tested:
Firmware/app version:
Tester:
State lights tested:
Patterns used:
Colour dependencies:
One-second recognition result:
Mis-press safety result:
Crash/reset result:
Sensory safety result:
Known exceptions:
```

## 18. Design note

SLS-1 is not anti-beauty.

It says beauty must not make the instrument harder or less safe to use.

Decorative lighting is allowed only when it cannot be mistaken for state, safety, write, arm, confirm, warning, or error information.
