# Repository Write Rules v0.1

This file is the canonical operating policy for repository writes across Merrin projects.

## Governing principle

Every solved GitHub failure should become institutional knowledge when its root cause and effective prevention are understood.

When a similar situation arises:

1. consult the established GitHub operating rules first;
2. apply the existing procedure;
3. record evidence of the result;
4. create or amend a rule only when the event reveals a genuinely new failure mode, root cause, safeguard, or recovery procedure.

Do not repeatedly rediscover solved problems. Do not create permanent rules from unexplained, transient, or one-off failures.

## Scope

These rules apply whenever ChatGPT, Codex, Work, automation, a connected tool, or a human operator creates or moves a Git branch or performs another repository write that depends on branch state.

## 1. Resolve the exact base before branch writes

Before creating or moving a branch:

1. identify the exact repository in `owner/name` form;
2. fetch the current intended base branch head;
3. record the full commit SHA;
4. pass that exact SHA to the write operation;
5. use one narrow, task-specific branch name.

Do not rely on an inferred, cached, remembered, or symbolic branch state when an exact commit SHA can be supplied.

## 2. One narrow operation at a time

Each repository write should perform one clearly described operation against one repository and one exact state.

Avoid vague write requests such as:

- create a working branch;
- start the next lane;
- branch from main;
- move the branch to the latest version.

Use requests equivalent to:

- create `feature/example-v0-1` in `owner/repository` from exact commit `<full-sha>`;
- move `feature/example-v0-1` to exact commit `<full-sha>` without force.

## 3. Recovery after a blocked write

A first blocked write is not automatically a project blocker.

Immediately retry once using:

- the exact repository;
- the freshly resolved full base commit SHA;
- one narrowly scoped operation;
- explicit non-destructive behaviour;
- no force update unless separately authorised.

Report a blocker only when this precise retry also fails, or when the failure reveals a genuine permission, policy, repository-state, or platform boundary.

## 4. Branch movement safeguards

Before moving an existing branch:

1. fetch the branch's current exact head;
2. fetch the intended target commit;
3. compare the two states where practical;
4. use a normal fast-forward update;
5. keep `force` disabled.

Force-moving, deleting, resetting, or overwriting a branch requires separate explicit authority and a recovery plan.

## 5. Evidence to record

For each branch creation or movement, retain:

- repository name;
- base branch or source purpose;
- exact source commit SHA;
- branch name;
- operation result;
- any blocked attempt and the result of the precise retry.

## 6. Failure-to-rule procedure

After a GitHub failure:

1. preserve the exact error and repository state;
2. determine whether an existing operating rule already covers it;
3. apply the established recovery procedure when one exists;
4. identify the root cause rather than documenting symptoms alone;
5. verify the proposed solution through a successful bounded operation;
6. add or amend a permanent rule only when the solution is evidenced and reusable;
7. record which earlier behaviour the new rule supersedes.

Each permanent entry should state:

- problem;
- symptoms;
- root cause;
- correct procedure;
- prevention;
- recovery path;
- evidence;
- date introduced;
- superseded rule or behaviour, where applicable.

## 7. Project adoption

Active repositories should contain either:

- a local copy of this policy at `.github/REPOSITORY_WRITE_RULES.md`; or
- a short `.github/REPOSITORY_WRITE_RULES.md` notice identifying Threadkeeper as the canonical source and recording any project-specific additions.

Local additions may strengthen this policy but must not weaken the exact-SHA, narrow-operation, non-force, blocked-write recovery, or institutional-learning rules.

## 8. Preflight committed JSON schemas and fixtures

Before exact-head review of a change that adds or modifies committed JSON schemas or fixtures:

1. run the repository's adopted JSON preflight command;
2. parse every selected file as strict UTF-8 JSON;
3. reject duplicate object keys;
4. validate schema documents against their adopted JSON Schema draft;
5. report only paths and structural locations, never parsed values or suspected secrets;
6. retain the complete semantic and regression test suite after preflight passes.

For Threadkeeper, the canonical command is:

```text
threadkeeper-schema-preflight
```

Threadkeeper continuous integration enforces this rule through the committed-tree regression in `tests/test_schema_preflight.py`.

A preflight failure is not authority to rewrite, delete, reset or bypass the affected record. Correct the narrow malformed or invalid file, rerun the preflight and then rerun the complete repository suite.

Adoption evidence:

- Unit G Issue #92;
- learning record `ml-4aa2890de62e90c37c6ca332f5b3a89aced22671b2ecbdb2ace76c04bd81e25d`;
- introduced 4 August 2026;
- rollback requires a separately reviewed retirement or supersession change.

## 9. Real-Thing Proof and completion status

This repository additionally consumes these exact authorities:

- Threadkeeper Real-Thing Proof authority: `armpitpete/threadkeeper@a5bc55336c86097301b378d8654ac92a26ef81e5`;
- Project Status v2 authority: `armpitpete/merrin-project-controls@7bc8b7f5ef921851ad163093f089d28d8128bf6c`;
- canonical semantic validator snapshot: `vendor/merrin-project-controls/7bc8b7f5ef921851ad163093f089d28d8128bf6c/validate_project_status.py`;
- canonical validator Git blob: `d0e704ab42d72da6b66fb1d9f31d739ed6220abd`.

The governing rule is:

> Never test a proxy when the claim concerns the real thing. Never allow `complete` to absorb implementation, deployment, live verification and human acceptance into one vague word.

For Merrin Open Synth Standards specifically:

- repository lifecycle status and individual standard maturity are separate evidence dimensions;
- `Draft`, `Freeze Candidate`, `Stable` and `Deprecated` describe the maturity of one standard, not the completion state of this repository;
- repository merge, CI or publication cannot substitute for real-use evidence required by a maturity claim;
- physical, player, accessibility and safety claims require direct evidence from the relevant real implementation or human surface;
- a `Stable` claim requires successful use across multiple independent implementation contexts and an evidence-backed review;
- automated validation may reject structurally unsupported maturity claims, but it must not manufacture real-world evidence or human acceptance.

Local rules may strengthen these boundaries but must not weaken the exact pinned authorities or their direct-evidence requirements.
