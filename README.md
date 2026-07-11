# Merrin Open Synth Standards

Practical draft standards for clearer, safer, more playable synth modules, browser synths, controllers, and performance instruments.

These standards began inside MerrinLab synth projects and are published here so they can be reused, adapted, criticised, and improved outside one repo.

They are not presented as universal law. They are working standards for builders who want consistent instrument behaviour.

## Standards

| Standard | Title | What it answers | Status |
|---|---|---|---|
| [MERRIN-STD-SLS-1](standards/MERRIN-STD-SLS-1_State_Lantern_System.md) | State Lantern System | What does this light mean? | Draft |
| [MERRIN-STD-HIL-1](standards/MERRIN-STD-HIL-1_Human_Interface_Layout.md) | Human Interface Layout | Where should this control, jack, LED, or performance area go? | Draft |

## Examples

| Example | Use |
|---|---|
| [Eurorack module example](examples/eurorack-module-example.md) | Shows SLS-1 and HIL-1 on a compact patchable module. |
| [Desktop controller example](examples/desktop-controller-example.md) | Shows hands-first layout, rear patching, and state-light placement. |
| [Browser synth example](examples/browser-synth-example.md) | Shows how the standards apply to Web Audio and HTML/CSS interfaces. |

## Repository files

- [Changelog](CHANGELOG.md)
- [Licence](LICENSE.md)
- [Notice](NOTICE.md)

## Core idea

Synths are not only circuits and code. They are also physical and visual decision systems.

A good instrument should make important states readable, keep risky actions obvious, and stop the player’s hands from fighting cables, tiny controls, or unclear lights.

## Scope

These standards are intended for:

- DIY synth modules
- Eurorack-style modules
- desktop synths
- browser synths
- MIDI/CV controllers
- performance surfaces
- hybrid software/hardware instruments

They are especially useful for small teams, solo builders, and AI-assisted synth projects where consistency can drift unless rules are written down.

## Standard summaries

### MERRIN-STD-SLS-1 — State Lantern System

Defines a shared LED/status-light language for instrument states.

It covers:

- canonical state names
- LED blink/breathe/steady patterns
- safety precedence
- destructive-action warning states
- sensory safety limits
- accessibility guidance
- compliance tests

Short version:

```text
State first.
Decoration second.
Rhythm carries meaning.
Colour reinforces meaning.
```

### MERRIN-STD-HIL-1 — Human Interface Layout

Defines practical layout rules for controls, jacks, LEDs, and performance areas.

It covers:

- knobs/controls above, jacks below as the default panel pattern
- patch cables kept away from the main hand area
- hands-first controller layout
- large controls for live movement
- grouped controls and jacks
- LED placement near the state it describes
- documented exceptions

Short version:

```text
The player’s hand should not fight the patch cables.
```

## Relationship between SLS-1 and HIL-1

```text
SLS-1 answers:
What does this light mean?

HIL-1 answers:
Where should this light/control/jack go?
```

Example:

```text
SLS-1 says a red triple pulse can mean CONFIRM REQUIRED.
HIL-1 says that LED must be near the affected control or system area, not hidden in decorative lighting.
```

## Versioning

Each standard has its own version and status.

Use this status language:

- `Draft` — open to change
- `Freeze Candidate` — believed stable, awaiting real use
- `Stable` — used successfully across multiple instruments
- `Deprecated` — replaced or no longer recommended

## Reuse

These standards are published under CC BY 4.0. You may share and adapt them with attribution.

## Attribution

Original concept, design, and drafting by Andy Rimmer / MerrinLab.

See [NOTICE.md](NOTICE.md).
