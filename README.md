# Merrin Open Synth Standards

Practical draft standards for clearer, safer, more playable synth modules, browser synths, controllers, and performance instruments.

These standards began inside MerrinLab synth projects and are published here so they can be reused, adapted, criticised, and improved outside one repo.

They are not presented as universal law. They are working standards for builders who want consistent instrument behaviour.

## Standards

| Standard | Title | What it answers | Version | Status |
|---|---|---|---|---|
| [MERRIN-STD-SLS-1](standards/MERRIN-STD-SLS-1_State_Lantern_System.md) | State Lantern System | What does this light mean? | v3.0-draft KISS candidate | Draft |
| [MERRIN-STD-HIL-1](standards/MERRIN-STD-HIL-1_Human_Interface_Layout.md) | Human Interface Layout | Where should this control, jack, LED, or performance area go? | current draft | Draft |

## Examples

| Example | Use |
|---|---|
| [Eurorack module example](examples/eurorack-module-example.md) | Shows SLS-1 and HIL-1 on a compact patchable module. |
| [Desktop controller example](examples/desktop-controller-example.md) | Shows hands-first layout, rear patching, and state-light placement. |
| [Browser synth example](examples/browser-synth-example.md) | Shows how the standards apply to Web Audio and HTML/CSS interfaces. |
| [SLS-1 v3 reference surface](examples/sls-1-reference/) | Executable colour + steady/slow/fast reference renderer. |
| [SLS-1 v3 recognition research](examples/sls-1-reference/recognition.html) | Retired browser-quiz evidence and current human-use model. |

## Repository files

- [Changelog](CHANGELOG.md)
- [Standard proposal process](docs/STANDARD_PROPOSAL_PROCESS.md)
- [SLS-1 v1/v2 → v3 migration](docs/SLS-1_V1_V2_TO_V3_MIGRATION.md)
- [SLS-1 v3 KISS candidate evidence](evidence/SLS-1_V3_KISS_CANDIDATE.md)
- [Licence](LICENSE.md)
- [Notice](NOTICE.md)

## Core idea

Synths are not only circuits and code. They are also physical and visual decision systems.

A good instrument should make important states noticeable, keep risky actions obvious, and stop the player’s hands from fighting cables, tiny controls, or unclear lights.

## MERRIN-STD-SLS-1 — State Lantern System

SLS-1 v3 deliberately rejects the Morse-like pulse vocabulary explored in v2.

The KISS rule is:

```text
Colour carries category.
Motion carries urgency.
Context carries exact local meaning.
```

The only temporal behaviours are:

```text
steady
slow flash
fast flash
```

No double pulse, triple pulse, short–long, long–short, or breathing state alphabet is canonical.

The normative v3 contract is:

```text
standards/data/sls-1-v3.0-kiss.json
```

A single unlabelled global light is deliberately limited to broad IDLE / ACTIVE / WARNING / ERROR communication. Exact critical action states require a second carrier such as a fixed label, position, text, symbol, or dedicated indicator.

### How indicators are learned

SLS-1 does not assume that a stranger should decode an exact state on first sight.

```text
see an indicator
→ investigate
→ read the key/manual
→ remember it next time
```

The indicator should make the condition noticeable and give a simple category/urgency cue. The label/context and documentation give the exact meaning.

Two unfamiliar-person browser quizzes were run during v3 design and both failed their artificial exact-naming criteria. They are preserved as research evidence. The second test showed that a one-second panel which disappears before the answer can measure visual search and short-term memory rather than realistic status-indicator use.

Abstract recognition quizzes are therefore **not** SLS-1 conformance gates.

## MERRIN-STD-HIL-1 — Human Interface Layout

HIL-1 defines practical layout rules for controls, jacks, LEDs, and performance areas.

Short version:

```text
The player’s hand should not fight the patch cables.
```

## Relationship between SLS-1 and HIL-1

```text
SLS-1 answers:
What does this light mean and how should its status convention work?

HIL-1 answers:
Where should this light/control/jack go?
```

Example:

```text
SLS-1 says ARMED uses the simple amber/steady category and needs contextual reinforcement.
HIL-1 says the ARMED indicator belongs next to the affected action/control, not hidden in decorative lighting.
```

## Versioning

Each standard has its own version and status.

- `Draft` — open to change
- `Freeze Candidate` — believed coherent and ready for bounded real use
- `Stable` — used successfully across multiple instruments or implementations
- `Deprecated` — replaced or no longer recommended

Material breaking changes require an explicit migration record and preserved access to the earlier version.

## Reuse

These standards are published under CC BY 4.0. You may share and adapt them with attribution.

## Attribution

Original concept, design, and drafting by Andy Rimmer / MerrinLab.

See [NOTICE.md](NOTICE.md).
