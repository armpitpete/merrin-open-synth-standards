# Standard Proposal Process

This process governs proposals for new Merrin Open Synth Standards and material changes to existing standards.

The aim is to make each standard useful, testable, open to criticism, and clear about its level of evidence. A proposal does not become accepted merely because it is well written or technically possible.

## 1. Start with a practical problem

Every proposal must identify:

- the instrument, interface, or workflow problem;
- who experiences the problem;
- the consequence of leaving it unresolved;
- existing approaches already considered;
- why a shared standard is more useful than a project-specific rule.

Do not begin with a preferred mechanism and invent the problem afterwards.

## 2. Define the proposal

A proposal must include:

- a unique working identifier;
- a plain-language title;
- intended scope;
- explicit exclusions;
- normative requirements;
- permitted exceptions;
- accessibility and safety consequences;
- at least one realistic implementation example;
- objective checks where practical;
- unresolved questions and known limitations.

Use `must` only for requirements necessary to claim compliance. Use `should` for strong recommendations and `may` for permitted choices.

## 3. Supply evidence

Evidence should be proportionate to the claim. It may include:

- use in a real instrument or prototype;
- player or builder observations;
- accessibility review;
- safety analysis;
- measurements;
- implementation comparisons;
- failure cases;
- compatibility tests.

A proposal must distinguish direct evidence, interpretation, design judgement, and unresolved uncertainty.

## 4. Review the draft

Review must ask:

1. Does the proposal solve the stated problem?
2. Can a builder understand and implement it?
3. Can compliance be checked without guessing?
4. Does it create avoidable cost, complexity, exclusion, or lock-in?
5. Are safety and accessibility requirements strong enough?
6. Does it conflict with an existing standard?
7. Are exceptions explicit rather than hidden?
8. Is the evidence strong enough for the proposed status?

Material findings must be corrected, explicitly accepted as limitations, or recorded as reasons to defer or reject the proposal.

## 5. Status progression

Use the repository's established status language:

- `Draft` — open to change and not yet proven sufficiently.
- `Freeze Candidate` — believed coherent and ready for bounded real use.
- `Stable` — used successfully across multiple instruments or implementations.
- `Deprecated` — replaced or no longer recommended.

A proposal normally moves one status at a time. Status is evidence about maturity, not a measure of importance.

### Maturity is not repository lifecycle

The maturity status above belongs to an individual standard. It must not be inferred from the repository's own lifecycle state.

In particular:

- a commit, pull-request merge, CI pass or publication on `main` can prove repository events but cannot by itself make a standard `Freeze Candidate` or `Stable`;
- `Freeze Candidate` requires bounded implementation or use evidence showing that the proposal has moved beyond documentation-only assertion, plus review appropriate to the claimed status; it may still be awaiting broader or player-facing real use;
- `Stable` requires successful use across multiple independent instrument or implementation contexts plus evidence-backed review;
- documentation can define player, accessibility, safety or physical requirements but cannot prove those requirements work in the real implementation;
- automated checks are supporting evidence and cannot substitute for human/player evidence where the claim concerns a human or physical surface;
- publication does not mean universal adoption, endorsement or implementation.

Future non-Draft maturity claims must provide the companion evidence record defined in `docs/REAL_THING_PROOF_CONSUMER_V0_1.md` at `evidence/maturity/<standard_id>.json`. The mechanical validator checks the minimum structure; review remains responsible for deciding whether the evidence really exercises the claimed environment and whether purported implementation contexts are genuinely independent.

## 6. Versioning and compatibility

Each accepted standard must have a stable identifier and explicit version.

A change is:

- **editorial** when meaning and compliance remain unchanged;
- **compatible** when existing compliant implementations remain compliant;
- **breaking** when an existing compliant implementation may no longer comply.

Breaking changes require:

- a new major version or replacement identifier;
- a migration note;
- the affected earlier version to remain available;
- an explicit compatibility statement;
- a reason the benefit outweighs disruption.

Do not silently rewrite a published requirement so that earlier implementations become non-compliant.

## 7. Decision outcomes

Review returns one outcome:

- `ACCEPT FOR CURRENT STATUS`
- `CORRECTIONS REQUIRED`
- `DEFER`
- `REJECT`

`DEFER` is appropriate when the idea may be sound but evidence, implementation proof, or review coverage is missing.

`REJECT` is appropriate when the proposal is outside scope, duplicates an existing standard without benefit, cannot be tested meaningfully, creates disproportionate harm or lock-in, or conflicts with the repository's purpose.

A rejected or deferred proposal should retain a short reason so the same unresolved idea is not repeatedly rediscovered.

## 8. Publication record

When a proposal is accepted, record:

- identifier and version;
- status;
- decision date;
- evidence reviewed;
- known limitations;
- compatibility classification;
- superseded standard, when applicable;
- changelog entry.

Publication does not imply universal adoption or endorsement. It means the proposal has passed the stated process for its recorded status.

## 9. Later changes

Changes to a published standard must follow the same evidence and review principles as a new proposal.

Small editorial corrections may use a narrow review. Material behavioural, safety, accessibility, compliance, or compatibility changes require a fresh proposal record and explicit status decision.
