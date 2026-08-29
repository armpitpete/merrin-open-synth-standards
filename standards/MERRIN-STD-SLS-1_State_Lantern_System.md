---
standard_id: MERRIN-STD-SLS-1
title: State Lantern System
version: v3.0-draft
status: Draft
scope: State and mode LEDs/status lights for synth modules, browser synths, controllers, and performance instruments.
license: CC-BY-4.0
machine_contract: standards/data/sls-1-v3.0-kiss.json
---

# MERRIN-STD-SLS-1 — State Lantern System

## 1. Purpose

SLS-1 defines a small, consistent visual language for instrument state.

The v3 KISS rule is:

> **Colour carries category. Motion carries urgency. Context carries exact local meaning.**

A player should not have to decode a Morse-like pulse alphabet to understand an instrument.

## 2. Human model

Indicators are learned interfaces.

The normal sequence is:

```text
notice an indicator
→ investigate what it means
→ read the product key/manual
→ remember the convention on later encounters
```

SLS-1 therefore does **not** require an unfamiliar person to infer an exact state name on first sight.

The indicator has three jobs:

1. make an important condition noticeable;
2. provide a simple category/urgency cue;
3. sit in enough context that the exact meaning can be looked up and learned.

The documentation has the complementary job of giving the exact meaning on first encounter.

This is the acceptance model for v3. A one-second blind recognition quiz is not a conformance gate.

## 3. Outcome

A compliant implementation should make important state noticeable, interpretable with its context/documentation, and progressively familiar through repeated use.

It must:

- use only the canonical semantic colours and three motion classes;
- avoid counted pulses, short–long codes, long–short codes, breathing alphabets, random flicker, and decorative state animations;
- use a label, symbol, position, shape, or other non-colour carrier for every critical state;
- keep state indication separate from meters and decorative activity;
- fail to IDLE or ERROR rather than falsely displaying ARMED, CONFIRM REQUIRED, or RECORD / WRITE;
- provide a static text/symbol equivalent for animated critical software indicators when reduced motion is requested;
- document the colour categories, motion categories, critical meanings, and local labels/symbols.

The design target is **simple learnability and consistent reuse**, not first-sight semantic guessing.

## 4. KISS vocabulary

### 4.1 Colours

| Colour | Meaning |
|---|---|
| White | neutral / idle |
| Green | normal / active |
| Blue | mode / informational state |
| Amber | attention / staged action |
| Red | write / fault category |

Colour is a category cue. It is never sufficient by itself for a critical state.

### 4.2 Motion

SLS-1 v3 permits exactly three temporal behaviours:

| Motion | Timing | Meaning |
|---|---:|---|
| Steady | no animation | state is present |
| Slow flash | 1000 ms cycle, 500 ms on | attention/action is required |
| Fast flash | 500 ms cycle, 250 ms on | urgent/fault condition |

No other temporal code is canonical.

SLS-1 v3 forbids double flashes, triple flashes, counted pulse groups, short–long or long–short signatures, breathing as a state code, random flicker, and strobe-like state signalling.

### 4.3 Context

Exact local meaning comes from the control/indicator context and documentation.

Examples:

- an amber steady light next to **ARM** tells the user that the ARM condition is active;
- an amber slow-flashing light next to **CONFIRM** tells the user that confirmation needs attention;
- a red steady light next to **WRITE** tells the user that the WRITE condition is active.

The lamp does not need to encode the words ARM, CONFIRM, or WRITE in its rhythm. The label already carries that information.

Do not force one anonymous lamp to encode a large state dictionary.

## 5. Canonical states

| State | Default visual |
|---|---|
| IDLE | white, dim, steady |
| ACTIVE | green, steady |
| ALT / SHIFTED | blue, steady |
| MUTED / BYPASSED | white, slow flash |
| ARMED | amber, steady |
| CONFIRM REQUIRED | amber, slow flash |
| RECORD / WRITE | red, steady |
| WARNING | amber, fast flash |
| ERROR | red, fast flash |
| CLOCK LOST | blue, slow flash |

The machine-readable source of truth is `standards/data/sls-1-v3.0-kiss.json`.

## 6. Single-indicator rule

A single **unlabelled global indicator** may communicate only broad category/state:

- IDLE;
- ACTIVE;
- WARNING;
- ERROR.

If an implementation needs ARMED, CONFIRM REQUIRED, RECORD / WRITE, CLOCK LOST, or another exact critical meaning, it must add a secondary carrier such as a fixed label or labelled position, text, a symbol/icon, a separate dedicated indicator, or another accessible non-colour cue.

Adding context is preferred to adding a more complicated blink language.

## 7. Precedence

When one global surface must choose among active states, highest precedence wins:

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

Precedence decides what is shown. It does not relax the secondary-carrier rule.

## 8. Risky/destructive action flow

For staged risky actions:

```text
safe state
↓ deliberate arm action
ARMED
↓ deliberate request to proceed
CONFIRM REQUIRED
↓ explicit confirmation
RECORD / WRITE while the operation actually occurs
↓
IDLE / ACTIVE on success
or
WARNING / ERROR on degraded/failing outcome
```

Lighting does not make an unsafe command safe. The command flow itself must remain deliberate.

## 9. Documentation and learning

Every conforming product must provide a concise indicator key in its normal documentation.

The key must identify:

- the product's SLS-1 colours and their categories;
- steady, slow-flash, and fast-flash meanings;
- every critical state used by the product;
- the label, symbol, or position associated with each critical indicator.

A user encountering an unfamiliar indicator should be able to investigate and determine its meaning without decoding a pulse sequence.

The intended learning effect is ordinary interface learning: after looking up a convention, later encounters should require less investigation.

SLS-1 does not require users to memorise the entire vocabulary before operating the product.

## 10. Accessibility and sensory safety

Critical states require at least one non-colour carrier in addition to colour/motion.

For software surfaces with reduced motion:

- animation must stop;
- critical meaning must remain available through text and/or symbol;
- the resulting state must remain visibly distinct.

No SLS-1 v3 pattern may exceed two visible on-events in any rolling second.

## 11. Human evidence

Abstract browser recognition quizzes are **research tools, not SLS-1 conformance gates**.

Two v3 research runs demonstrated why:

- a blind anonymous-light test scored 17/21 (81.0%) and mainly failed on exact action-state naming;
- a complete labelled-panel test shown for one second and hidden before answer scored 14/21 (66.7%), indicating the harness had become a visual-search/short-term-memory task rather than a realistic indicator-use task.

These failures remain valid negative evidence for those exact test designs. They do not justify adding more flash patterns.

Human evidence should instead come from realistic implementations and ask:

1. Is an important state noticeable during normal use?
2. When unfamiliar, can the user find and understand the explanation?
3. Does the documentation resolve the exact meaning correctly?
4. Does repeated use make the convention easier to recognise without increasing code complexity?

A browser mock-up may help answer these questions, but it must not substitute an artificial memory test for real use.

## 12. Conformance boundary

Repository validation can prove that the v3 machine contract is internally consistent and keeps the KISS vocabulary bounded.

It cannot prove noticeability on every physical product, colour discrimination for every user, physical LED performance, ambient-light performance, hardware crash/brownout behaviour, player acceptance, learning retention, or multi-implementation adoption.

SLS-1 remains **Draft** while implementation evidence accumulates. Independent review may assess the specification before such implementation evidence exists, provided claims remain inside this boundary.
