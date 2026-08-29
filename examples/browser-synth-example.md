# Example — Browser Synth

This example shows how a browser-based synth can apply SLS-1 v3 and HIL-1.

It is illustrative, not human-recognition evidence.

## App

```text
Example name: Focused Browser Voice
Format: Web Audio instrument
Inputs: on-screen keyboard, computer keyboard, optional Web MIDI
Main functions: play voice, shape tone, show status, provide panic/stop
```

## HIL-1 layout principle

A browser synth should separate the public instrument surface from diagnostics.

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

## SLS-1 v3 state examples

| Behaviour | State | Expression |
|---|---|---|
| App ready | IDLE | white dim steady + `Ready` |
| Audio running | ACTIVE | green steady + `Audio running` |
| Alternate keyboard layer | ALT / SHIFTED | blue steady + `Shift` |
| Muted voice | MUTED / BYPASSED | white slow flash + `Muted` |
| About to overwrite setting | ARMED | amber steady + `Armed` |
| Waiting for confirmation | CONFIRM REQUIRED | amber slow flash + `Confirm` |
| Saving local setting | RECORD / WRITE | red steady + `Writing` |
| MIDI degraded/unavailable | WARNING | amber fast flash + warning text |
| Audio/MIDI fault | ERROR | red fast flash + error text/panic guidance |
| Expected clock lost | CLOCK LOST | blue slow flash + `Clock lost` |

The text is not decorative redundancy: for critical states it is the required secondary carrier.

## Accessibility

Do not rely on colour alone for critical meaning.

When reduced motion is requested, stop animation and retain text/symbol state.

## Common mistake

Weak design:

```text
The app opens with raw MIDI logs, debug switches, and a clever multi-pulse light code.
```

Better design:

```text
The app opens as an instrument. Important state is obvious through colour, simple motion, and plain context.
```
