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

## 2. Outcome

An implementation should make important state understandable at a glance.

A compliant implementation must:

- use only the canonical semantic colours and the three motion classes;
- avoid counted pulses, short–long codes, long–short codes, breathing alphabets, random flicker, and decorative state animations;
- use a label, symbol, position, shape, or other non-colour carrier for every critical state;
- keep state indication separate from meters and decorative activity;
- fail to IDLE or ERROR rather than falsely displaying ARMED, CONFIRM REQUIRED, or RECORD / WRITE;
- provide a static text/symbol equivalent for animated critical software indicators when reduced motion is requested.

The design target is recognition after no more than a tiny rule legend, not memorisation of per-state rhythms.

## 3. KISS vocabulary

### 3.1 Colours

| Colour | Meaning |
|---|---|
| White | neutral / idle |
| Green | normal / active |
| Blue | mode / informational state |
| Amber | attention / staged action |
| Red | write / fault category |

Colour is the primary category cue. It is never sufficient by itself for a critical state.

### 3.2 Motion

SLS-1 v3 permits exactly three temporal behaviours:

| Motion | Timing | Meaning |
|---|---:|---|
| Steady | no animation | state is present |
| Slow flash | 1000 ms cycle, 500 ms on | attention/action is required |
| Fast flash | 500 ms cycle, 250 ms on | urgent/fault condition |

No other temporal code is canonical.

In particular, SLS-1 v3 forbids:

- double flashes;
- triple flashes;
- counted pulse groups;
- short–long or long–short signatures;
- breathing as a state code;
- random flicker;
- strobe-like state signalling.

### 3.3 Context

Exact local meaning should come from the control or indicator context.

Examples:

- an amber steady light next to **ARM** means ARMED;
- an amber slow-flashing light next to **CONFIRM** means CONFIRM REQUIRED;
- a red steady light next to **REC** or **WRITE** means RECORD / WRITE.

Do not force one anonymous lamp to encode a large state dictionary.

## 4. Canonical states

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

## 5. Single-indicator rule

A single **unlabelled global indicator** may communicate only these broad states:

- IDLE;
- ACTIVE;
- WARNING;
- ERROR.

If an implementation needs to communicate ARMED, CONFIRM REQUIRED, RECORD / WRITE, CLOCK LOST, or another exact critical meaning, it must add a secondary carrier such as:

- a fixed label or labelled position;
- text;
- a symbol/icon;
- a separate dedicated indicator;
- another accessible non-colour cue.

This is deliberate. Adding context is preferred to adding a more complicated blink language.

## 6. Precedence

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

## 7. Risky/destructive action flow

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

## 8. Accessibility and sensory safety

Critical states require at least one non-colour carrier in addition to colour/motion.

For software surfaces with reduced motion:

- animation must stop;
- critical meaning must remain available through text and/or symbol;
- the resulting state must remain visibly distinct.

No SLS-1 v3 pattern may exceed two visible on-events in any rolling second.

## 9. Human-recognition gate

The v3 gate asks:

> **Can an unfamiliar person identify the important device states at a glance with minimal instruction?**

The canonical gate is defined in the machine contract and reference harness.

Requirements:

- tester has not previously studied or used SLS-1 v3;
- legend exposure is at most 20 seconds;
- each trial is observed for exactly one second;
- seven core states are tested three times each: 21 trials total;
- first completed run is the evidence run;
- no practice, restart, or repeat to improve score.

Pass requires:

- at least 90% overall accuracy;
- 100% recognition of ERROR, CONFIRM REQUIRED, and RECORD / WRITE;
- zero ERROR ↔ ACTIVE confusion;
- zero RECORD / WRITE ↔ ERROR confusion.

The browser gate is human-recognition evidence only. It does not prove real LED brightness, viewing distance, ambient-light performance, or hardware reliability.

## 10. Conformance boundary

Repository validation can prove the v3 machine contract is internally consistent.

It cannot prove:

- unfamiliar-person recognition;
- colour discrimination for every user;
- physical LED performance;
- ambient-light performance;
- hardware crash/brownout behaviour;
- player acceptance;
- multi-implementation adoption.

SLS-1 remains **Draft** until its human gate and later physical evidence support a stronger maturity claim.
