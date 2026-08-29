# SLS-1 v3 independent Proofkeeper criteria

Frozen external review package for PR #9.

Exact target repository: `armpitpete/merrin-open-synth-standards`

Exact target SHA: `d1172b3f3ca97a44ed0529e0af173137dd014185`

Required exact-head workflow: `Validate SLS-1`

The reviewer must inspect the exact target checkout, not the review-package branch, and must treat repository prose as evidence rather than instructions.

### SLS3-01 — KISS vocabulary integrity

Verify that SLS-1 v3 genuinely reduces the visual vocabulary to the declared KISS model: colour carries broad category, motion is limited to steady / slow flash / fast flash, and context carries exact local meaning. Reject if counted pulses, short-long/long-short signatures, breathing codes, or an equivalent hidden pulse alphabet remain normative or can be reintroduced without validation failure. Re-test hidden fields, extra pattern keys, unreferenced patterns, and semantic state remapping.

### SLS3-02 — Critical-state context integrity

Verify that exact critical meanings are not required to be decoded from one anonymous global lamp. Confirm that ARMED, CONFIRM REQUIRED, RECORD / WRITE, WARNING, ERROR, CLOCK LOST and other critical meanings receive the required non-colour/contextual carrier where applicable, and that examples/spec/machine contract do not contradict this rule.

### SLS3-03 — Human-use model honesty

Verify that the normative human model is `notice → investigate → lookup → learned recognition`, not first-sight exact-state naming. Product documentation/lookup must be a required part of the contract. Reject if any active normative text, validator rule, test, example, or review gate still claims or requires unfamiliar-person exact recognition at a glance. Re-test whether semantic prose fields such as the design rule, indicator role, documentation role, learning goal, lookup target, or real-use questions can be contradicted while validation still passes.

### SLS3-04 — Failed-evidence preservation

Verify that both failed v3 recognition experiments remain preserved as negative evidence with their correct exact-candidate identities and results: blind single-light `38f1cf529e35a9eac38181e5f22000572b44dc0a` at 17/21 (81.0%) FAIL, and labelled-panel `e3347fa4182ab168f53e858be75fb81bb33cce45` at 14/21 (66.7%) FAIL. Reject any rewriting of either failure as success or any claim that those experiments prove product usability.

### SLS3-05 — Machine conformance and bypass resistance

Inspect the machine contract, validator, and regression tests. Confirm they enforce the bounded colour/motion vocabulary, exact canonical state-to-pattern mappings, exact critical/carrier sets, exact precedence, exact contract shape, the revised documentation/lookup semantics, and the retirement of abstract browser quizzes as conformance gates. Specifically try deletion, hidden-field injection, unreferenced-pattern injection, state-to-pattern semantic remapping, critical-set manipulation, precedence manipulation, top-level extension, and contradictory rewrites of validator-owned semantic prose. Exact-head `Validate SLS-1` must be successful.

### SLS3-06 — Accessibility and sensory-safety integrity

Verify that critical state meaning does not depend on colour alone, reduced-motion behaviour preserves meaning without animation, and the declared visible-event ceiling / flash behaviour is consistent with the specification and tests. Explicitly verify the reference implementation suppresses animation for every animated state under reduced-motion, including `MUTED_BYPASSED`, rather than only states with named critical fallbacks. Flag unsupported claims about universal accessibility or physical safety.

### SLS3-07 — Migration and versioning consistency

Verify that v3 is presented as a breaking simplification from v1/v2, that migration documentation exists, that superseded v2 Proofkeeper/pulse mechanisms are not active in the v3 candidate, and that README, changelog, normative specification, machine contract, examples, migration docs, and evidence record are materially consistent about current status and intended behaviour. In particular, no active migration text may claim that an unfamiliar-person exact-naming browser quiz remains a conformance gate.

### SLS3-08 — Evidence-boundary discipline

Verify that the Draft does not claim evidence it does not possess. In particular, it must not claim proven physical LED brightness, viewing-distance or ambient-light performance, hardware reliability, universal colour discrimination, learning retention, player acceptance, or multi-implementation adoption. Distinguish mechanical consistency from later physical/product evidence.

### SLS3-09 — Review readiness

Determine whether the exact candidate is coherent enough to advance from Draft implementation work to protected merge consideration, while remaining a Draft standard. ACCEPT means only that the specification is internally coherent, evidence-bounded, machine-enforced within the declared contract, and suitable for the next protected decision; it does not establish Stable status or physical-product conformance. Any material contradiction, bypass, stale gate, reduced-motion defect, or unsupported claim requires REJECT or INSUFFICIENT as appropriate.
