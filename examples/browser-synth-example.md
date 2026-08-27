# Example — Browser Synth

This example shows how a browser-based synth can apply SLS-1 v2 and HIL-1.

It is illustrative. For executable SLS-1 behaviour, see [`sls-1-reference/`](sls-1-reference/).

## App

```text
Example name: Focused Browser Voice
Format: Web Audio instrument
Inputs: on-screen keyboard, computer keyboard, optional Web MIDI
Main functions: play voice, shape tone, show status, provide panic/stop
```

## HIL-1 layout principle

A browser synth should separate the public instrument surface from diagnostics.

Recommended page order:

```text
instrument title and short purpose
↓
play/panic/status row
↓
main performance controls
↓
keyboard or performance surface
↓
simple visual feedback
↓
advanced/test/diagnostic section collapsed by default
```

## Suggested browser layout

```text
[ Title: Focused Browser Voice ]
[ Status: Ready ] [ Start Audio ] [ Panic ]

MAIN CONTROLS
Tone | Fade | Weight | Space

PLAY AREA
on-screen keyboard / pads / gesture surface

STATE
active note, mode, warning/error text

ADVANCED / TEST
MIDI diagnostics, raw event log, effect toggles, debug state
```

## HIL-1 notes

- The first visible controls should be playable controls, not debug tools.
- Panic/stop should remain easy to find.
- MIDI diagnostics should be available but not visually dominant.
- State text should appear near the related behaviour.
- Keyboard/touch targets should be large enough for normal use.
- Debug panels should not make the app look unfinished if the user arrives cold.

## SLS-1 for browser UI

SLS-1 can be implemented with LED-like indicators, status chips, icon/text blocks, or small state badges.

The state resolver is independent of rendering.

| Behaviour | SLS-1 state | Normal expression |
|---|---|---|
| App loaded but audio not started | IDLE | P0 + `Ready` |
| Audio running | ACTIVE | P1 + `Audio running` |
| Alternate keyboard layer | ALT / SHIFTED | P2 + `Shift` |
| Muted voice | MUTED / BYPASSED | P3 + `Muted` |
| About to overwrite setting | ARMED | P5 + `Armed` |
| Waiting for second confirmation | CONFIRM REQUIRED | P6 + `Confirm` |
| Saving local setting | RECORD / WRITE | P4 + `Writing` |
| MIDI degraded/unavailable | WARNING | P7 + warning text |
| Audio/MIDI fault | ERROR | P8 + error text and panic guidance |
| Expected external clock lost | CLOCK LOST | P9 + `Clock lost` |

## Accessibility notes

Do not rely only on colour.

Use at least two relevant carriers across the complete control:

- text label;
- rhythm/animation;
- placement near relevant control;
- icon;
- brightness/weight;
- screen-reader-visible status text.

When `prefers-reduced-motion: reduce` is active, critical animated states must have a static equivalent such as:

```text
A  Armed
!  Confirm
W  Writing
△  Warning
×  Error
C  Clock lost
```

The underlying SLS-1 state and precedence do not change.

## Compliance notes

```text
HIL-1:
- Main controls visible before diagnostics: design intent
- Panic accessible: design intent
- Status near relevant controls: design intent
- Debug/test controls visually separated: design intent

SLS-1:
- State meanings documented: yes
- Browser expressions map to v2 canonical states: yes
- Colour not the only signal: yes
- Reduced-motion critical fallback defined: yes
- Human recognition test: not performed in this illustrative example
```

## Common mistake

Weak design:

```text
The app opens with raw MIDI logs, debug switches, and test controls above the playable instrument.
```

Better design:

```text
The app opens as an instrument. Diagnostics are available behind an advanced/test section.
```
