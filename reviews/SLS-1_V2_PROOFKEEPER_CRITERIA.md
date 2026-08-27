# SLS-1 v2.0-draft — frozen independent semantic review criteria

Review target: the exact pull-request head containing this file.

Purpose: adversarially determine whether the SLS-1 v2.0-draft candidate is internally coherent, implementable, evidence-disciplined, and safe enough to merge as a **Draft**. This review does not decide human recognition, physical acceptance, Freeze Candidate promotion, Stable status, merge authority, or deployment authority.

For every criterion below, inspect the exact repository evidence rather than relying on PR prose. A material contradiction is `FAIL`. Missing evidence required to decide a criterion is `INSUFFICIENT`.

### SLS-01 — Problem, scope, and breaking-version discipline

PASS requires all of the following:

- the v2 standard still solves the stated status-language problem rather than expanding into unrelated instrument behaviour;
- the change from v1 is correctly classified as breaking where normative timing/mappings changed;
- migration guidance exists;
- the earlier v1 draft remains specifically recoverable;
- the candidate does not silently present v1 implementations as v2 compliant.

Inspect at minimum:

- `standards/MERRIN-STD-SLS-1_State_Lantern_System.md`
- `docs/SLS-1_V1_TO_V2_MIGRATION.md`
- `docs/STANDARD_PROPOSAL_PROCESS.md`

### SLS-02 — One-second critical signature claim is structurally true

PASS requires the prose and machine contract to agree that every critical global temporal pattern has a complete repeating cycle of no more than 1000 ms, and the validator must actually reject a longer critical cycle.

The review must distinguish this structural timing property from human one-second recognition. The repository must not claim the former proves the latter.

Inspect at minimum:

- `standards/MERRIN-STD-SLS-1_State_Lantern_System.md`
- `standards/data/sls-1-v2.0-patterns.json`
- `scripts/validate_sls1.py`
- `tests/test_sls1.py`

### SLS-03 — Critical global patterns form a defensible small vocabulary

PASS requires canonical, non-cyclically-equivalent defaults for:

- ERROR;
- CONFIRM REQUIRED;
- ARMED;
- RECORD / WRITE;
- WARNING;
- CLOCK LOST.

ERROR must not depend on brightness alone. WARNING must not remain implementation-defined. CLOCK LOST must not share the global MUTED/BYPASSED pattern. The validator must enforce the critical uniqueness claim rather than merely documenting it.

Inspect at minimum the v2 standard, machine contract, validator, and regression tests.

### SLS-04 — Resolver precedence and global/local semantics are coherent

PASS requires:

- one deterministic resolver model;
- documented global precedence;
- global safety truth not being contradicted by local indicators;
- locally reused non-critical patterns being allowed only where context such as label/position carries the distinction;
- single-indicator instruments being treated as global;
- the executable resolver agreeing with the normative precedence.

Look for stale-state or equal-precedence behaviour that could make the global indicator oscillate or lie.

Inspect at minimum:

- `standards/MERRIN-STD-SLS-1_State_Lantern_System.md`
- `standards/data/sls-1-v2.0-patterns.json`
- `examples/sls-1-reference/sls.mjs`
- `tests/test_sls_reference.mjs`

### SLS-05 — Staged risky/destructive flow fails safe

PASS requires the standard to make clear that indication does not itself make a dangerous command safe and that staged operations behave as a sequence rather than decorative labels.

Specifically:

- ARMED must not execute the operation;
- CONFIRM REQUIRED must require deliberate confirmation;
- cancel/timeout must return to a safe non-writing state;
- timeout must never execute;
- RECORD / WRITE must be shown only while the operation is actually occurring;
- failure must resolve to an honest WARNING or ERROR as appropriate;
- crash/reset/brownout must not manufacture or blindly restore ARMED/CONFIRM/WRITE state.

Inspect the normative standard and updated examples.

### SLS-06 — Accessibility and reduced-motion semantics preserve truth

PASS requires:

- colour not being the sole state carrier;
- critical state distinctions not relying on colour plus brightness alone;
- software reduced-motion rendering preserving the same canonical state and precedence while removing required temporal animation;
- static critical fallbacks having meaningful text and/or symbol information;
- no claim that SLS-1's internal pulse ceiling automatically proves conformance with every external flashing/accessibility threshold.

Inspect at minimum the standard, machine contract, browser reference, and evidence record.

### SLS-07 — Mechanical validation tests the claims it says it tests

PASS requires the validator/tests to meaningfully exercise, not merely restate:

- mandatory mappings;
- cycle/segment consistency;
- rolling one-second pulse ceiling;
- critical cycle limit;
- cyclic critical uniqueness;
- canonical WARNING/ERROR/ARM/CONFIRM/WRITE/CLOCK LOST mappings;
- static critical reduced-motion fallbacks.

At least one hostile regression must demonstrate rejection for each major failure family rather than only checking the valid fixture.

Passing CI is supporting regression evidence, not semantic proof by itself.

### SLS-08 — Human recognition gate is reproducible without being pre-claimed

PASS requires the repository to provide a bounded recognition protocol/harness that:

- starts temporal samples at random phase;
- exposes the indicator for one second before the answer;
- tests every critical state at least ten times;
- records state, answer, correctness and phase;
- calculates the stated overall and prohibited-confusion gates;
- preserves a reproducible seed or equivalent trial identity;
- clearly says an unperformed run is not PASS;
- clearly distinguishes browser-simulation human evidence from physical-hardware evidence.

The review must reject any fabricated or pre-populated human PASS claim.

Inspect:

- `standards/MERRIN-STD-SLS-1_State_Lantern_System.md`
- `examples/sls-1-reference/recognition.html`
- `examples/sls-1-reference/recognition.mjs`
- `tests/test_sls_reference.mjs`
- `evidence/SLS-1_V2_COMPLETION_EVIDENCE.md`

### SLS-09 — Examples and repository summaries do not inflate conformance

PASS requires the README, changelog, browser example, desktop-controller example, and Eurorack example to agree with v2 mappings and to distinguish design intent/illustration from performed human or physical conformance evidence.

Reject stale v1 mappings presented as current v2 guidance or illustrative `yes` fields that falsely imply a performed real-world test.

### SLS-10 — Maturity and evidence claims remain bounded

PASS requires:

- SLS-1 to remain `Draft` in this candidate;
- mechanical proof to be separated from human recognition, player acceptance, ambient-light/physical viewing, real destructive-action mis-press behaviour, hardware crash/brownout behaviour, and multi-implementation adoption;
- no Freeze Candidate or Stable claim from repository/CI evidence alone;
- no merge, deployment, publication, credential, spending, or owner-acceptance authority to be granted by this review package.

Inspect at minimum:

- `standards/MERRIN-STD-SLS-1_State_Lantern_System.md`
- `README.md`
- `CHANGELOG.md`
- `evidence/SLS-1_V2_COMPLETION_EVIDENCE.md`
- `docs/STANDARD_PROPOSAL_PROCESS.md`
