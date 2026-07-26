# Testing and Validation Governance

Apply the selected mode contract first. In a read-only mode, use this guidance only to inspect, prove, and report; do not execute the repair, convergence, or check-creation steps.

Use tests and runtime checks as evidence of preserved outcomes, not ceremony after editing.

## Build the verification matrix first

| Behavior | Primary evidence | Boundary evidence |
|---|---|---|
| Pure invariant/policy | Unit or table-driven test | Caller/contract test when mapping matters |
| Service/use case | Component/unit with real domain logic | Integration test for transaction/adapter |
| Persistence/query | Database/repository integration test | Query plan/benchmark/lock evidence |
| HTTP/API/event contract | Handler/contract/consumer test | End-to-end and mixed-version compatibility |
| Job/queue workflow | Handler test with failure/idempotency cases | Delivery/state-effect integration test |
| UI interaction | Component test | Browser flow for route/network/feedback/accessibility |
| Migration/cross-service change | Migration/schema/contract test | Staged environment, reconciliation, rollback/roll-forward |
| Runtime reliability | Reproduction plus SLI/log/trace evidence | Post-fix observation window and threshold |

## Baseline before writable change

When feasible:

- Reproduce the bug or capture a failing check.
- Run directly relevant existing checks.
- Record pre-existing and flaky failures separately.
- Capture before-state UI/API/job/runtime evidence.
- Identify commands that write generated files, caches, databases, snapshots, or shared state.

If a test cannot fail before the fix, explain why and use characterization/invariant evidence instead.

## Required checks after change

Run in increasing scope by risk:

1. Direct regression/changed test.
2. Related module/package suite.
3. Relevant type/lint/format/static checks.
4. Integration/contract/database/migration checks for changed boundaries.
5. Build/package/artifact checks.
6. API/UI/job smoke or end-to-end flow for externally visible behavior.
7. Architecture fitness, compatibility, release, and runtime-observation checks required by the risk class.
8. Repository-wide checks only when repository policy or blast radius requires them.

Also inspect final diff/status, changed callers, untested branches, contract/schema/migration behavior, resource cleanup, logs/console/network failures, and rollback.

## Independent verification

`verify` must:

- Identify the exact artifact/diff being accepted.
- Derive expected behavior independently from authoritative sources.
- Inspect tests for implementation mirroring and missing negative/boundary cases.
- Reproduce evidence where safe rather than trusting a repair report.
- Avoid modifying code/tests when a check fails.
- Return `VERIFIED`, `PARTIAL`, `FAILED`, `BLOCKED`, or `UNKNOWN` with proof.

The same Agent may perform implementation and a later verification pass, but it must re-orient from the artifact and acceptance sources rather than treating its previous conclusion as evidence.

## Read-only command safety

In read-only modes, run only commands known to be observational or isolated. Test runners may update snapshots, databases, lockfiles, coverage files, or generated source; inspect documented behavior and use disposable environments. If safety cannot be established, do not run the command and mark the check `blocked`/`not run`.

## Evidence integrity

For every check record exact command/flow, working directory/environment, target revision/version, result, and relevant summary. Use only:

- `passed`
- `failed`
- `blocked`
- `not run`

A build is not a behavioral test; a mocked unit test is not a contract proof; HTTP 200 is not a business-success proof; a short observation window cannot prove long-cycle reliability.

## Test quality

Tests must assert outcomes/invariants, cover the original failure boundary, include negative/boundary/retry/idempotency/permission cases when relevant, avoid duplicating the production rule in setup, remain deterministic, and fail for the intended reason.

## Completion rule

A repair is `verified` only when risk-required checks pass. A release is `READY` only when target-specific mandatory gates pass. An operational repair needing runtime evidence remains `partial` until its defined observation window and thresholds are evaluated.
