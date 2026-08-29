# SLS-1 v3 KISS candidate evidence

## Decision

The v2 72-trial Morse-like recognition gate is superseded before Proofkeeper review.

Reason: the design required users to distinguish counted and ordered pulse signatures. The v3 candidate applies KISS instead of spending evidence effort proving that complexity can be learned.

The later v3 browser quizzes are also now **research evidence, not conformance gates**.

## v3 design change

- Colour carries category.
- Motion is limited to steady, slow flash, fast flash.
- Context carries exact local meaning.
- Counted pulses, short/long signatures, and breathing codes are forbidden.
- A single unlabelled global indicator is deliberately limited to IDLE / ACTIVE / WARNING / ERROR.
- Exact critical states require a second carrier such as label, position, text, symbol, or dedicated indicator.

## Human-use model

The accepted model is:

```text
notice an indicator
→ investigate
→ read the product key/manual
→ remember the convention next time
```

An unfamiliar user is not expected to infer an exact semantic state name from a light on first sight.

The indicator should be noticeable and simple. Documentation supplies the exact first-encounter meaning. Consistent reuse produces familiarity.

## Research run 1 — blind single light — FAIL

Exact candidate: `38f1cf529e35a9eac38181e5f22000572b44dc0a`

First completed unfamiliar-person run:

- 17/21 correct — 81.0%;
- IDLE 3/3;
- ACTIVE 3/3;
- ARMED 3/3;
- CONFIRM REQUIRED 1/3;
- RECORD / WRITE 1/3;
- WARNING 3/3;
- ERROR 3/3;
- one prohibited RECORD / WRITE ↔ ERROR confusion.

Verdict under that research protocol: **FAIL**.

Finding: broad categories worked, but stripping away contextual carriers made exact action-state naming unreliable.

## Research run 2 — labelled panel hidden after one second — FAIL

Exact candidate: `e3347fa4182ab168f53e858be75fb81bb33cce45`

First completed run by a different unfamiliar tester:

- 14/21 correct — 66.7%;
- IDLE 2/3;
- ACTIVE 2/3;
- ARMED 2/3;
- CONFIRM REQUIRED 3/3;
- RECORD / WRITE 2/3;
- WARNING 1/3;
- ERROR 2/3;
- zero prohibited ERROR ↔ ACTIVE confusions;
- zero prohibited RECORD / WRITE ↔ ERROR confusions.

The submitted seed `1594027353` reproduced the trial order, phases, slot assignments, state counts, and score. The evidence is structurally valid.

Verdict under that research protocol: **FAIL**.

Finding: adding labels fixed CONFIRM REQUIRED to 3/3, but hiding the entire six-position panel after one second turned the task into visual search plus short-term recall. The protocol was no longer a faithful model of persistent status indicators.

## Resulting correction

Do **not** add more pulse vocabulary and do **not** keep rerunning abstract unfamiliar-person naming quizzes.

The normative v3 human model is now notice → investigate → lookup → learned recognition.

Abstract browser quizzes are not conformance gates. Future human evidence should come from realistic implementations and ask whether important states are noticed, whether users can find and understand the explanation, and whether the convention becomes easier to recognise through ordinary use.

## Evidence boundary

Repository tests can verify the bounded colour/motion vocabulary, critical-state context requirements, documentation requirement, and human-use model.

They cannot prove real-world noticeability, physical LED brightness, ambient-light performance, accessibility for every user, learning retention, or player acceptance.

Independent review may assess this specification inside those stated boundaries. Physical and longitudinal human evidence belongs to implementation maturity, not to an abstract pre-review quiz.
