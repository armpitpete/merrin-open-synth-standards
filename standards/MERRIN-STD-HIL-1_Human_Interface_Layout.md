---
standard_id: MERRIN-STD-HIL-1
title: Human Interface Layout
version: v1.0-draft
status: Draft
scope: Physical and visual placement of controls, jacks, LEDs, labels, and performance areas.
license: CC-BY-4.0
---

# MERRIN-STD-HIL-1 — Human Interface Layout

## 1. Purpose

HIL-1 defines practical layout rules for synth modules, browser synths, controllers, and performance instruments.

It exists because many instruments become harder to play when:

- patch cables cross the main hand area
- jacks interrupt live controls
- LEDs are far from the state they describe
- dangerous controls are too easy to hit
- small switches hide important mode changes
- diagnostic controls look like performance controls
- labels are unreadable in normal use

HIL-1 is a human-interface standard, not a circuit-placement rule.

It answers:

```text
Where should this control, jack, light, label, or performance area go so the instrument remains playable?
```

## 2. Core principle

```text
The player’s hand should not fight the patch cables.
```

The playing surface belongs to the player.

Patching, service access, diagnostics, and destructive controls must not interfere with normal performance.

## 3. Scope

### Applies to

HIL-1 applies to:

- module panels
- desktop synths
- controller surfaces
- browser synth layouts
- MIDI/CV interfaces
- performance instruments
- jack placement
- control grouping
- LED placement
- label placement
- diagnostic/control separation

### Does not apply to

HIL-1 is not a complete standard for:

- PCB component placement
- high-voltage safety layout
- RF layout
- EMC/EMI compliance
- thermal design
- manufacturing tolerances
- enclosure mechanical drawings

Those may need separate engineering standards.

## 4. Default panel pattern

For normal module panels, use Pattern A unless there is a documented reason not to.

```text
Pattern A:
Controls above.
Jacks below.
```

Rationale:

- hands reach controls without pushing through patch cables
- cable flow is predictable
- labels remain easier to read
- performance controls stay visually primary
- patching stays functional but not dominant

## 5. Pattern A layout

Recommended vertical order:

```text
Title / identity
↓
main performance controls
↓
secondary controls / switches
↓
state LEDs near affected controls
↓
patch jacks
```

For compact panels, preserve the principle even if the exact row structure changes.

## 6. Exceptions

Exceptions are allowed, but must be documented.

Each exception should answer:

```text
What rule is being broken?
Why is the exception needed?
How does the design still protect playability?
```

Valid reasons may include:

- very small module width
- format-specific constraints
- banana-jack workflows
- Buchla/Serge-style layout conventions
- safety isolation
- cable strain relief
- RF/audio separation
- desktop controller ergonomics
- accessibility improvement

Invalid reasons include:

- it looked cool
- there was space left
- copying another panel without checking usability
- hiding complexity by scattering controls

## 7. Hands-first performance zones

Performance surfaces should reserve clear zones for the hands.

Do not place jacks, toggle forests, or cable paths where they block:

- finger movement
- palm movement
- pressure gestures
- slides
- repeated live adjustment
- singing/standing posture
- visual confirmation of state

For two-hand instruments, separate left-hand and right-hand zones clearly.

Example performance-surface rule:

```text
Playable surface in the centre.
Patch/service edge at the rear, side, or lower edge.
```

## 8. Jack placement

### 8.1 Default jack rule

Put patch jacks where cables naturally leave the playing area.

Preferred positions:

- bottom edge for vertical modules
- rear edge for desktop controllers
- rear/lower edge for angled performance surfaces
- side edge only when it reduces cable crossing

Avoid:

- jacks between closely related live controls
- jacks in the middle of a gesture surface
- jacks above frequently used knobs unless format demands it
- jack rows that obscure labels once patched

### 8.2 Jack grouping

Group jacks by function.

Recommended group order:

1. timing inputs
2. pitch/CV inputs
3. modulation inputs
4. audio inputs
5. audio outputs
6. gate/trigger outputs
7. expression/performance outputs
8. service/utility connections

For controller surfaces, a signal-story order may be clearer:

```text
time enters → pitch/harmony leaves → expression leaves → events leave → accidents/special states leave
```

Document the chosen order.

## 9. Control placement

### 9.1 Main controls

Main controls should be:

- larger than rarely used controls
- reachable without moving cables
- grouped by musical function
- labelled in normal playing orientation
- placed where accidental movement is unlikely

### 9.2 Dangerous or destructive controls

Dangerous controls include:

- erase
- overwrite
- save-to-flash
- record/write
- reset
- calibration commit
- high-gain feedback
- output-level jumps

These controls should use at least one protection method:

- hold action
- two-step confirm
- recessed placement
- guarded switch
- separated location
- clear SLS-1 state light
- screen/text confirmation
- timeout after arming

### 9.3 Diagnostic controls

Diagnostic/test controls should not look like normal performance controls.

Place them in:

- advanced section
- test panel
- collapsed browser section
- rear/service area
- labelled utility group

Do not let diagnostics dominate the instrument face.

## 10. LED placement

LEDs should be placed near the thing they describe.

Rules:

- a state LED belongs next to the affected control, channel, jack group, or function area
- a global LED belongs near the title, power area, or top-level status area
- warning/error LEDs must be visible from normal playing position
- decorative lights must be visually distinct from state lights
- SLS-1 state lights must not be hidden inside decorative clusters

If using SLS-1, HIL-1 requires that LED meaning and placement agree.

Example:

```text
If an LED signals ARMED for a write button, it must be near that write action, not elsewhere on the panel.
```

## 11. Label placement

Labels should be readable in normal use.

Rules:

- labels should not be covered by inserted cables
- labels should be near the relevant control or jack
- abbreviations should be documented
- destructive controls should use plain labels, not clever names only
- browser controls should use readable text, not only icons
- live controls should keep names short enough to scan

Preferred label hierarchy:

```text
instrument name
section names
control names
state/action labels
technical details
```

## 12. Browser synth layout

For browser synths and web instruments:

- keep the main playing controls visible without scrolling where possible
- hide diagnostics unless needed
- keep status text near relevant controls
- preserve keyboard/touch target size
- provide panic/stop access if audio or MIDI can hang
- make the live/playable area visually distinct from test controls
- do not make debug panels look like the public instrument

## 13. Desktop controller layout

For desktop or angled controller surfaces:

- put hands in the centre
- put patching at rear or lower rear edge
- avoid cable paths over sensors
- avoid cable paths over palm zones
- support comfortable wrist angle
- support sitting and standing where relevant
- do not force the player to hunch if singing or performing live
- keep left/right hand roles readable

Recommended physical structure:

```text
player side
↓
main hand/performance surface
↓
secondary controls
↓
rear/lower rear patch edge
```

## 14. Performance surface rule

A performance surface is not a normal rack module.

If a device is meant for broad hand, palm, touch, gesture, or pressure performance, do not squeeze the main surface into a narrow vertical module just to fit a format.

Acceptable architecture:

```text
performance surface
↓
breakout cable / rear jack box
↓
Eurorack / CV / MIDI / audio system
```

This keeps the player’s hands clear while preserving modular compatibility.

## 15. Control grouping

Group controls by what the player is trying to do, not only by circuit topology.

Useful grouping types:

- voice
- pitch
- tone
- envelope
- space
- memory/echo
- timing
- routing
- safety
- diagnostics
- expression
- performance scenes

Avoid scattering related controls across the face unless there is a strong performance reason.

## 16. Accessibility and stress-use rules

A good layout should still work when the player is tired, overloaded, in low light, or mid-performance.

Rules:

- avoid tiny gotcha switches for important actions
- avoid mode states that are invisible
- make mute/bypass states clear
- make destructive states hard to trigger accidentally
- keep live controls reachable without precision strain
- make stop/panic controls easy to find
- do not rely on colour alone
- leave space around frequently used controls

## 17. Relation to SLS-1

HIL-1 and SLS-1 are separate but compatible.

```text
SLS-1 defines what state lights mean.
HIL-1 defines where those lights should go.
```

A design is weak if the LED language is good but the LED is placed where the player cannot associate it with the affected function.

## 18. Compliance checklist

A project claiming HIL-1 conformance should answer:

```text
HIL-1 conformance
Date reviewed:
Project/version:
Reviewer:
Default pattern used:
Documented exceptions:
Main controls reachable without cable interference: yes/no
Jacks grouped by function: yes/no
State LEDs near affected controls/functions: yes/no
Dangerous controls protected: yes/no
Diagnostics visually separated: yes/no
Labels readable when patched: yes/no
Panic/stop accessible where needed: yes/no
Known layout risks:
```

## 19. Simple pass/fail tests

### Test 1 — cable interference

Patch the likely normal-use cables.

Pass if the main controls can still be adjusted without the hand fighting cables.

### Test 2 — one-glance state association

Ask what each visible state light belongs to.

Pass if the user can associate each state LED with its function without reading a manual.

### Test 3 — destructive-action safety

Try to operate the instrument casually.

Pass if destructive controls cannot be hit accidentally during normal performance.

### Test 4 — low-light use

Use the instrument in dim light.

Pass if the main controls, panic/stop action, and warning/error states remain understandable.

### Test 5 — diagnostics separation

Look at the instrument from normal playing position.

Pass if test/debug controls do not appear to be the main instrument surface.

## 20. Design note

HIL-1 does not ban unusual layouts.

It requires unusual layouts to explain themselves.

A strange layout can be good if it protects playability, hand movement, state clarity, and performance safety.
