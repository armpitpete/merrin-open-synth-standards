# SLS-1 v3 independent Proofkeeper review criteria

Target candidate: `52fe6fa7c08af647b324ed396861edd0db9248f5`

This file is review control material, not candidate evidence. The reviewer must inspect the exact target checkout and treat this file only as the frozen falsification contract.

The review is deliberately bounded to repository-provable claims. It must not infer physical LED brightness, ambient-light performance, universal accessibility, learning retention, or player acceptance from repository evidence.

This is a fresh re-review after predecessor `89ff776f0da1421b6fdda581171e157b7c9f0909` was rejected for duplicate JSON object-member ambiguity. The reviewer must independently retest that bypass and adjacent parser/consumer exactness routes; the prior verdict neither proves nor disproves the corrected candidate.

A criterion is PASS only when the exact target evidence establishes it. Material contradiction is FAIL. Missing evidence is INSUFFICIENT. Any FAIL forces overall REJECT. Otherwise any INSUFFICIENT forces overall INSUFFICIENT. Only all PASS permits ACCEPT.

### V3-01 — KISS temporal vocabulary is genuinely bounded

The normative SLS-1 v3 contract must limit temporal behaviour to exactly steady, slow flash, and fast flash. Counted pulse groups, ordered short/long signatures, breathing state codes, random flicker, and decorative state animation must not remain available as canonical semantic encodings through prose, data, examples, renderer behaviour, aliases, or validation loopholes.

### V3-02 — Colour, motion, and context responsibilities are coherent

The exact candidate must consistently implement the rule that colour carries broad category, motion carries urgency, and context carries exact local meaning. A single unlabelled global indicator must remain limited to broad IDLE / ACTIVE / WARNING / ERROR communication. Exact critical meanings such as ARMED, CONFIRM REQUIRED, RECORD / WRITE, and CLOCK LOST must require a secondary carrier such as label, position, text, symbol, or dedicated indicator rather than another blink word.

### V3-03 — Safety and reduced-motion constraints survive the simplification

The KISS rewrite must not weaken safety semantics. Inspect precedence, visible-event rate limits, critical-state treatment, secondary-carrier requirements, and reduced-motion fallbacks across normative prose, machine data, validator logic, reference implementation, and tests. Contradictory fallback text/symbol mappings, weakened precedence, non-canonical event ceilings, or routes around required context are failures.

### V3-04 — The human-use model matches the preserved evidence

The candidate must consistently state the intended progression as notice → investigate → lookup/read documentation → learned recognition, without claiming that unfamiliar users can name exact states from a bare light on first sight. Both failed browser-recognition protocols must remain preserved as negative research evidence and must not be silently converted into conformance PASS evidence. The candidate must explain why those abstract quizzes are no longer conformance gates without claiming that their failures did not occur.

### V3-05 — Documentation is a real normative dependency

Product documentation must be required strongly enough to supply exact first-encounter meaning. The normative contract and validator must require documentation of the colour categories, motion categories, critical meanings, local labels/symbols or equivalent contextual carriers, and the lookup route needed by the human-use model. Examples or prose must not imply that documentation is optional where the contract depends on it.

### V3-06 — Normative prose, machine contract, validator, renderer, and tests agree

The Markdown standard, `standards/data/sls-1-v3.0-kiss.json`, `scripts/validate_sls1.py`, the reference implementation, and the regression suites must describe and enforce the same v3 semantics. Look specifically for aliases, ordering/duplicate loopholes, type-coercion loopholes, renderer behaviour that exceeds the contract, stale v2 assumptions, and tests that prove only a weaker rule than the prose claims.

### V3-07 — Supersession and migration are honest and non-destructive

The repository must present v3 as a breaking/superseding draft rather than pretending v2 never existed or claiming Stable maturity. The migration and changelog material must preserve the reason for abandoning the v2 Morse-like architecture and must not misstate the two failed v3 research protocols. Earlier evidence may be superseded in authority but must remain intelligible as historical evidence.

### V3-08 — Repository evidence boundaries are explicit and respected

The candidate may claim repository-verifiable consistency, bounded vocabulary, context requirements, documentation requirements, and the declared human-use model. It must not promote those checks into proof of physical brightness, ambient-light performance, noticeability in every implementation, accessibility for every user, longitudinal learning retention, or player acceptance. Any such overclaim is a failure.

### V3-09 — Exact-head mechanical evidence is valid

`.proofkeeper-runtime/workflow-runs.json` must show a completed successful `Validate SLS-1` pull-request workflow for exact target SHA `52fe6fa7c08af647b324ed396861edd0db9248f5`. A successful run for another SHA, a pending/cancelled run, or absence of the required exact-head run is not PASS.

### V3-10 — No material semantic bypass remains

Adversarially inspect the complete candidate for a practical route that would let an implementation claim SLS-1 v3 conformance while reintroducing forbidden temporal vocabulary, overloading the single global indicator, omitting required critical-state context/documentation, weakening reduced-motion/safety meaning, or otherwise satisfying mechanical tests while violating the written contract. Explicitly retest duplicate JSON object members at top-level and nested levels, then probe adjacent parsing and consumer-divergence cases. PASS requires no material bypass supported by the exact repository evidence.
