---
standard_id: MERRIN-STD-SLS-1
title: State Lantern System
version: v2.0-draft
status: Draft
scope: State and mode LEDs/status lights for synth modules, browser synths, controllers, and performance instruments.
license: CC-BY-4.0
machine_contract: standards/data/sls-1-v2.0-patterns.json
---

# MERRIN-STD-SLS-1 — State Lantern System

## 1. Purpose

SLS-1 defines a compact, consistent language for lights and equivalent status indicators used by musical instruments.

It exists to stop each module, controller, synth, or app inventing a private meaning for steady lights, pulses, warnings, confirmation states, and faults.

A player should not have to guess whether a light means:

- active;
- muted;
- armed;
- awaiting confirmation;
- recording or writing;
- warning;
- error;
- clock loss;
- decorative activity.

SLS-1 treats state indication as part of instrument behaviour, not decoration.

## 2. Outcome

An SLS-1 implementation should make important state readable quickly and safely.

A compliant implementation must:

- expose behavioural state rather than hide it;
- give higher-risk states priority over ordinary activity;
- use a small documented vocabulary;
- make colour optional reinforcement rather than the only information carrier;
- keep state indication separate from meters and decorative animation;
- fail to IDLE or ERROR rather than falsely displaying ARMED, CONFIRM REQUIRED, or RECORD / WRITE;
- keep critical global pattern identity available within every rolling one-second observation window;
- provide a non-animated equivalent for critical animated states on software surfaces when reduced motion is requested.

The one-second recognition target applies to the **complete rendered state**: rhythm, label, position, symbol, brightness, and text may all contribute. Critical global states have the stronger requirement that the pattern itself repeats its complete cyclic signature within one second.

## 3. Scope

### 3.1 Applies to

SLS-1 applies to any indicator communicating:

- state;
- mode;
- arm/confirm flow;
- record/write/save state;
- mute/bypass state;
- warning;
- error;
- transport or clock state;
- safety condition.

The indicator may be:

- a physical LED;
- an LED ring segment;
- a lamp;
- an HTML/CSS status indicator;
- an icon or status chip;
- a screen status region;
- another clearly state-bearing visual element.

### 3.2 Does not apply to

SLS-1 does not govern:

- purely decorative lighting;
- audio meters;
- clipping meters;
- signal-present indicators;
- aesthetic animation clearly separated from state signalling.

Decorative or activity indications must never override, mask, or imitate safety state indications.

### 3.3 Relationship to broader safety/accessibility standards

SLS-1 is an instrument-domain convention, not a replacement for general safety or accessibility standards.

Implementers remain responsible for applicable requirements such as:

- IEC 60073 coding principles for indicators and actuators;
- WCAG flashing limits on web/software surfaces;
- platform accessibility and reduced-motion behaviour.

SLS-1 deliberately uses a simple ceiling of no more than three visible on-pulses in any rolling one-second window. This is an internal design invariant; it does not by itself prove conformance with every external flashing definition or threshold.

## 4. Core principles

1. **State before decoration.** A state indicator must communicate behaviour, not merely look active.
2. **Rhythm carries risk meaning.** Critical states must not depend on colour or brightness alone.
3. **Colour only reinforces.** A colour change may add meaning but must not be the sole carrier.
4. **Context may carry low-risk meaning.** Position, label, brightness, or screen text may distinguish ordinary local states.
5. **Critical global patterns are unique.** ERROR, CONFIRM REQUIRED, ARMED, RECORD / WRITE, WARNING, and CLOCK LOST must not share cyclically equivalent patterns on a global indicator.
6. **Readable quickly.** Important state should be identifiable in one second or less at normal use distance.
7. **No hidden behavioural change.** If behaviour changes materially, relevant state must become visible.
8. **Fail safe.** Reset, crash, brownout, or ambiguity must never manufacture a risky state.
9. **Small alphabet.** Reuse named patterns rather than inventing decorative variations.
10. **Safety outranks activity.** Risk information wins precedence.

## 5. Definitions

| Term | Meaning |
|---|---|
| State indicator | A visual element communicating behavioural state rather than audio level. |
| Global indicator | An indicator summarising the highest-precedence state across an instrument or system. |
| Local indicator | An indicator whose position/label gives it a specific local meaning. |
| Pulse | One visible on-event followed by return to off/low state. |
| Pattern cycle | The repeating duration of a temporal pattern. |
| Cyclic signature | The ordered on/off durations that identify a repeating pattern, independent of where observation begins in the cycle. |
| Critical global state | ERROR, CONFIRM REQUIRED, ARMED, RECORD / WRITE, WARNING, or CLOCK LOST. |
| Breathe | Smooth brightness change with no hard blink edge. |
| Reduced-motion equivalent | A static label/symbol/weight presentation carrying the same state without temporal animation. |
| Dim | Low but readable steady intensity. |
| Mid | Ordinary readable steady intensity. |
| Bright | High readable intensity; brightness alone is not sufficient for a critical distinction. |

## 6. Canonical states

### 6.1 Mandatory core states

| Display name | Machine token | Meaning |
|---|---|---|
| IDLE | `IDLE` | Default safe state; nothing engaged or awaiting action. |
| ACTIVE | `ACTIVE` | Function/path/mode is engaged. |
| ALT / SHIFTED | `ALT_SHIFTED` | Alternate layer is active. |
| MUTED / BYPASSED | `MUTED_BYPASSED` | Path/output intentionally suppressed. |
| ARMED | `ARMED` | Risky/high-impact action staged but not yet executable. |
| CONFIRM REQUIRED | `CONFIRM_REQUIRED` | Explicit final confirmation is required now. |
| RECORD / WRITE | `RECORD_WRITE` | A record/write/save/commit operation is actually in progress. |
| WARNING | `WARNING` | Non-fatal issue; degraded or risky behaviour is possible. |
| ERROR | `ERROR` | Fault requiring user action or preventing correct/safe behaviour. |

### 6.2 Optional clock/transport states

| Display name | Machine token | Meaning |
|---|---|---|
| CLOCK PRESENT | `CLOCK_PRESENT` | External clock detected and in use. |
| CLOCK LOST | `CLOCK_LOST` | Expected external clock missing or invalid. |
| TRANSPORT RUN | `TRANSPORT_RUN` | Sequencer/transport running. |
| TRANSPORT STOP | `TRANSPORT_STOP` | Sequencer/transport stopped but ready. |

### 6.3 Optional focus states

| Display name | Machine token | Meaning |
|---|---|---|
| SELECTED / FOCUSED | `SELECTED_FOCUSED` | Channel, part, scene, or parameter is under edit. |
| LOCKED / HELD | `LOCKED_HELD` | A latched state persists until deliberately cleared. |

## 7. Pattern contract

The normative machine-readable pattern contract is:

```text
standards/data/sls-1-v2.0-patterns.json
```

If prose and the machine contract disagree on exact timing, the discrepancy is a specification defect. Neither silently overrides the other; conformance must stop until the mismatch is corrected.

### 7.1 Sensory safety invariant

No SLS-1 state pattern may exceed:

```text
3 visible on-pulses in any rolling 1000 ms window
```

No state pattern may use random flicker, strobe-like behaviour, or meter-like animation.

### 7.2 Critical signature invariant

Every critical global pattern must have a complete repeating cycle of:

```text
1000 ms or less
```

This closes the v1.0 failure where a two-second pattern could leave a player watching a blank/ambiguous phase for more than one second.

### 7.3 Canonical v2 patterns

| ID | Name | Cycle | Rhythm / expression | Default use |
|---|---|---:|---|---|
| P0 | `STEADY_DIM` | steady | dim steady | IDLE |
| P1 | `STEADY_MID` | steady | mid steady | ACTIVE |
| P2 | `BREATHE_SLOW` | 2000 ms | smooth breathe | ALT / SHIFTED, focus |
| P3 | `PULSE_LONG_1HZ` | 1000 ms | 420 ms on, 580 ms off | MUTED / BYPASSED |
| P4 | `PULSE_SHORT_1HZ` | 1000 ms | 160 ms on, 840 ms off | RECORD / WRITE |
| P5 | `DOUBLE_EQUAL_1HZ` | 1000 ms | 140 on, 140 off, 140 on, 580 off | ARMED |
| P6 | `TRIPLE_EQUAL_1HZ` | 1000 ms | 110 on/off repeated as three pulses, then rest | CONFIRM REQUIRED |
| P7 | `WARNING_SHORT_LONG` | 1000 ms | 120 on, 140 off, 300 on, 440 off | WARNING |
| P8 | `ERROR_LONG_SHORT` | 1000 ms | 300 on, 140 off, 120 on, 440 off | ERROR |
| P9 | `CLOCK_LOST_WIDE_DOUBLE` | 1000 ms | 120 on, 520 off, 120 on, 240 off | CLOCK LOST |

Exact segment durations are normative in the machine contract.

### 7.4 Why WARNING and ERROR are temporal

v1.0 allowed WARNING to be locally invented and defaulted ERROR to steady bright. That made warning vocabulary inconsistent and could reduce ERROR versus ACTIVE to brightness perception.

v2 therefore gives both states canonical rhythms:

```text
WARNING = short → long
ERROR   = long → short
```

Brightness and colour may reinforce these patterns but may not replace them on a global indicator.

### 7.5 Colour

SLS-1 does not assign mandatory colours.

An implementation may use conventional colours, but the state must remain distinguishable without colour through at least one additional carrier such as:

- rhythm;
- text;
- symbol;
- position;
- shape;
- tactile grouping.

For a critical state, colour plus brightness alone is insufficient.

## 8. Forbidden patterns and mappings

Non-compliant behaviour includes:

- more than three visible on-pulses in any rolling second;
- critical pattern cycles longer than one second;
- strobe or near-strobe animation;
- random flicker on a state indicator;
- meter-like animation on a state indicator;
- decorative blinking that can be mistaken for state;
- local WARNING patterns invented when the canonical WARNING pattern is practical;
- ERROR distinguished from ACTIVE only by brightness;
- colour-only state differences;
- a global indicator using cyclically equivalent patterns for two critical states;
- displaying RECORD / WRITE when no write/record/save/commit operation is actually occurring.

## 9. State precedence

When multiple states apply to the same global indicator, highest precedence wins:

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

Optional local states such as SELECTED / FOCUSED and LOCKED / HELD may be rendered locally without displacing a higher global safety state.

## 10. Tie-break rules

If multiple states at the same precedence exist:

1. show the state with greater documented severity;
2. if equal, show the most recent;
3. if equal, prefer the selected/focused target for a local indicator;
4. if still equal, use a documented deterministic implementation order.

A global indicator must never oscillate between equal states merely because two subsystems update at different rates.

## 11. Global and local indicators

### 11.1 Global indicator

A global indicator must:

- show the highest-precedence applicable state;
- use the canonical pattern for each critical global state unless an explicit documented exception is necessary;
- keep all critical global patterns mutually distinguishable;
- not contradict a local safety truth.

### 11.2 Local indicator

A local indicator may reuse a non-critical pattern where its location or label makes meaning unambiguous.

Example:

```text
A steady mid light next to OSC 2 may mean OSC 2 active.
A steady mid light next to CLOCK may mean clock present.
```

That reuse is acceptable because the local label carries part of the meaning.

Critical local states should use the canonical critical pattern unless the hardware cannot render it. An exception must document the alternative carrier that prevents ambiguity.

### 11.3 Single-indicator instruments

If the instrument has only one state indicator, treat it as global.

## 12. Required state-to-pattern map

Default map:

| State | Pattern |
|---|---|
| IDLE | P0 `STEADY_DIM` |
| ACTIVE | P1 `STEADY_MID` |
| ALT / SHIFTED | P2 `BREATHE_SLOW` |
| MUTED / BYPASSED | P3 `PULSE_LONG_1HZ` |
| RECORD / WRITE | P4 `PULSE_SHORT_1HZ` |
| ARMED | P5 `DOUBLE_EQUAL_1HZ` |
| CONFIRM REQUIRED | P6 `TRIPLE_EQUAL_1HZ` |
| WARNING | P7 `WARNING_SHORT_LONG` |
| ERROR | P8 `ERROR_LONG_SHORT` |
| CLOCK LOST | P9 `CLOCK_LOST_WIDE_DOUBLE` |

A compliant implementation must publish its state map and any exceptions.

## 13. Risky/destructive action flow

SLS-1 does not make an unsafe command safe merely by lighting an LED. The command flow itself must be deliberate.

For an action requiring staged confirmation, use this behavioural sequence:

```text
safe state
↓ deliberate arm action
ARMED
↓ deliberate request to proceed
CONFIRM REQUIRED
↓ explicit confirm within documented window
RECORD / WRITE while operation is actually occurring
↓
IDLE / ACTIVE on success
or
WARNING / ERROR on degraded/failing outcome
```

### 13.1 ARMED

ARMED means:

- a risky action has been staged;
- the action must not yet execute;
- cancellation must return to a safe state.

### 13.2 CONFIRM REQUIRED

CONFIRM REQUIRED means:

- the system is waiting for a specific deliberate confirmation;
- the confirmation window must be documented;
- if the window expires, the system must return to a safe non-writing state;
- timeout must not execute the action.

A two-second confirmation window is the default recommendation where no domain-specific timing is required.

### 13.3 RECORD / WRITE

RECORD / WRITE must be displayed only while the operation is actually happening.

If the operation fails:

- use WARNING if the system remains usable but degraded;
- use ERROR if the operation cannot be trusted or safe behaviour cannot be verified.

Reset, crash, or brownout must never resume at ARMED or CONFIRM REQUIRED without re-establishing the real underlying state.

## 14. Implementation rules

### 14.1 Single resolver

Do not let subsystem animations compete directly.

Use:

```text
collect active states
↓
resolve precedence
↓
select effective state
↓
select canonical/local pattern
↓
render
```

The reference resolver in `examples/sls-1-reference/` demonstrates this model.

### 14.2 Boot/reset fail-safe

During boot, reset, or unknown state:

- show IDLE if safe state is verified;
- show ERROR if safe state cannot be verified;
- never show ARMED, CONFIRM REQUIRED, or RECORD / WRITE unless that state is true.

### 14.3 Brightness

Brightness must be:

- visible at normal playing distance;
- usable in low light;
- not painfully bright at close range;
- consistent within one instrument.

Brightness may reinforce state but is not enough by itself to distinguish critical states.

### 14.4 Activity separation

State indicators must not behave as audio meters.

If state and activity must share one physical light, state precedence wins and meter/activity animation must stop while a state requiring the indicator is shown.

## 15. Accessibility and reduced motion

### 15.1 Multiple carriers

Do not make colour the only signal.

Use at least two relevant carriers across the complete interface:

- rhythm;
- label;
- position;
- shape/icon;
- brightness;
- screen text;
- tactile grouping.

### 15.2 Software reduced motion

When the operating environment exposes a reduced-motion preference, a software SLS-1 implementation must provide a non-animated equivalent for critical animated states.

The v2 machine contract defines default text/symbol fallbacks.

Example:

```text
normal:
double pulse + "Armed"

reduced motion:
static "A  Armed"
```

Reduced motion changes **rendering**, not the underlying canonical state or precedence.

### 15.3 Hardware

Hardware that supports user display preferences should provide a lower-motion/static mode where practical.

Very simple hardware without such preferences may continue to use canonical rhythm, but critical meaning must still have a second contextual carrier such as label, position, or adjacent screen text.

## 16. Conformance tests

Conformance has separate mechanical and human evidence. Passing machine checks does not prove human recognition.

### Test A — machine pattern invariants

Run:

```text
python scripts/validate_sls1.py
```

Pass criteria:

- all mandatory states mapped;
- exact pattern cycle totals valid;
- no pulse pattern exceeds three on-pulses in any rolling second;
- every critical global pattern has a cycle of one second or less;
- critical global patterns are not cyclically equivalent;
- canonical WARNING and ERROR patterns exist;
- critical states have static reduced-motion fallbacks.

### Test B — resolver precedence

Run the reference resolver tests.

Pass criteria:

- ERROR outranks every lower state;
- CONFIRM REQUIRED outranks ARMED;
- deterministic IDLE fallback;
- reduced-motion presentation retains state identity.

### Test C — one-second human recognition

Goal: identify rendered state in one second or less at normal playing distance.

Protocol:

1. familiarise the tester with the legend for no more than one minute;
2. start each temporal sample at a random phase, not only at pattern onset;
3. include all mandatory states;
4. present each critical state at least ten times;
5. record response and response time before revealing correctness.

Pass criteria for one bounded implementation:

- 90% or better recognition overall;
- 100% correct for ERROR, ARMED, CONFIRM REQUIRED, and RECORD / WRITE;
- zero ARMED/WARNING confusion;
- zero ERROR/ACTIVE confusion.

One tester may support a bounded prototype decision but does not prove general human performance. Stable status requires stronger real-use evidence across implementations.

### Test D — mis-press safety

Goal: accidental destructive actions do not occur under distracted use.

Pass criteria:

- zero accidental destructive actions across 20 attempts;
- ARMED appears before final confirmation;
- CONFIRM REQUIRED appears only when confirmation is genuinely possible;
- timeout/cancel returns to safe state;
- timeout never executes the action.

### Test E — crash/reset fail-safe

Pass criteria:

- safe verified recovery displays IDLE/ACTIVE as appropriate;
- unverifiable recovery displays ERROR;
- no false ARMED, CONFIRM REQUIRED, or RECORD / WRITE after recovery.

### Test F — sensory safety

Pass criteria:

- validator passes rolling-window pulse ceiling;
- no random flicker;
- no strobe-like state behaviour;
- software rendering also meets applicable platform/web flashing requirements.

### Test G — reduced-motion equivalence

On a software implementation with reduced motion enabled:

- critical state remains visible;
- temporal animation is not required to identify the state;
- text/symbol state agrees with resolver truth;
- precedence remains unchanged.

## 17. Required conformance record

Each implementing project should record:

```text
SLS-1 conformance
Standard version:
Date tested:
Firmware/app version:
Implementation:
Tester:
State indicators tested:
State map:
Pattern contract version/hash:
Machine validator result:
Resolver result:
Random-phase recognition result:
Mis-press safety result:
Crash/reset result:
Sensory safety result:
Reduced-motion result:
Colour dependencies:
Known exceptions:
Evidence locations:
```

Do not mark an unperformed test as PASS.

## 18. Reference implementation

`examples/sls-1-reference/` contains a small browser implementation that:

- loads the normative pattern JSON;
- resolves simultaneous states by canonical precedence;
- renders the selected pattern;
- exposes critical reduced-motion fallbacks.

It is an executable reference and mechanical test surface.

It is **not**, by itself:

- evidence of player recognition;
- physical-hardware evidence;
- proof of accessibility acceptance;
- proof of adoption by an instrument.

## 19. Version compatibility

v2.0 is a breaking draft revision of v1.0 because it changes normative pattern timing and default mappings.

The published v1.0-draft remains recoverable from repository history at commit:

```text
11ecdeb3f2c27db09d065e3bca69746a3d83b7c9
```

Migration guidance is recorded in:

```text
docs/SLS-1_V1_TO_V2_MIGRATION.md
```

Do not claim v1.0 conformance as v2.0 conformance without retesting.

## 20. Known limitations

SLS-1 v2 remains Draft until direct evidence justifies promotion.

Known limits:

- machine uniqueness does not guarantee human perceptual uniqueness;
- the reference browser implementation is not a finished musical instrument;
- very small single-LED hardware may need documented exceptions;
- different ambient lighting and viewing distances require implementation-level testing;
- no colour palette is standardised;
- auditory or tactile state languages are outside the current scope.

## 21. Design note

SLS-1 is not anti-beauty.

Decorative lighting is welcome when it cannot be mistaken for state, warning, write, arm, confirmation, or error information.

The governing rule is:

```text
State first.
Decoration second.
Risk must never be pretty enough to become ambiguous.
```
