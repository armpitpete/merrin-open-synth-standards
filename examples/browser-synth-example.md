# Example — Browser Synth

This example shows how a browser-based synth can apply SLS-1 and HIL-1.

It is illustrative, not mandatory.

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

The same state logic applies even if the “light” is rendered in HTML/CSS.

| Behaviour | SLS-1 state | Browser expression |
|---|---|---|
| App loaded but audio not started | IDLE | dim status badge / `Ready` |
| Audio running | ACTIVE | steady active badge / `Audio running` |
| Alternate keyboard layer | ALT / SHIFTED | slow breathe or clear `Shift` state |
| Muted voice | MUTED / BYPASSED | slow pulse / `Muted` |
| About to overwrite setting | ARMED | double pulse / `Armed` |
| Waiting for second confirmation | CONFIRM REQUIRED | triple pulse / `Confirm` |
| Saving local setting | RECORD / WRITE | 1Hz pulse / `Saving` |
| MIDI unavailable | WARNING | non-fatal warning text and state marker |
| Audio/MIDI stuck | ERROR | bright/error status and panic guidance |

## Accessibility notes

Do not rely only on colour.

Use at least two of:

- text label
- rhythm/animation
- placement near relevant control
- icon
- brightness/weight
- screen-reader-visible status text

Respect reduced-motion preferences where possible.

## Compliance notes

```text
HIL-1:
- Main controls visible before diagnostics: yes
- Panic accessible: yes
- Status near relevant controls: yes
- Debug/test controls visually separated: yes
- Touch/keyboard targets usable: yes

SLS-1:
- State meanings documented: yes
- Browser status chips map to canonical states: yes
- Colour not the only signal: yes
- Warning/error states visible: yes
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
