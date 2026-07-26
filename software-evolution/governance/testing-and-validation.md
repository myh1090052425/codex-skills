# Testing and Validation Governance

Use tests as evidence of preserved behavior and repaired risk, not as a ceremony after editing.

## Build a verification matrix before change

Map each affected behavior to the lowest useful test and required boundary checks:

| Behavior | Primary evidence | Boundary evidence |
|---|---|---|
| Pure rule/invariant | Unit or table-driven test | Caller/contract test when mapping matters |
| Service/use case | Unit/component test with real domain logic | Integration test for transaction or external adapter |
| Persistence/query | Repository/database integration test | Query plan/benchmark for performance claims |
| HTTP/API contract | Handler/contract test | End-to-end or consumer compatibility check |
| Event/job workflow | Handler test with idempotency/error cases | Integration test for delivery/state effect |
| UI state/interaction | Component test | Browser flow for routing/network/user feedback |
| Cross-service/data migration | Contract/migration test | Staged environment validation and rollback proof |

## Baseline

Before editing when feasible:

- Reproduce the bug or capture a failing test.
- Run directly relevant existing tests.
- Record pre-existing failures and flaky behavior.
- Capture runtime/API/UI behavior needed for before/after comparison.

If a regression test cannot fail before the fix, explain why and use a characterization or invariant test instead.

## Required checks after change

Run in increasing scope according to risk:

1. Changed test or direct regression test.
2. Related package/module test suite.
3. Type checker, linter, formatter check, and static analysis relevant to the changed files.
4. Integration/contract/database tests for changed boundaries.
5. Build/package checks.
6. API/UI/job smoke or end-to-end flow for externally visible behavior.
7. Repository-wide checks only when risk or repository policy requires them.

Also inspect:

- Final `git diff` and `git diff --check` when Git exists.
- Changed callers and untested branches.
- Contract/schema/migration compatibility.
- Logs, console/network failures, and resource cleanup for runtime changes.

## Verification integrity

Record exact command, working directory/environment, result, and relevant summary. Use only these statuses:

- `passed`: command/flow ran and met the criterion.
- `failed`: command/flow ran and did not meet it.
- `blocked`: required dependency/environment/permission was unavailable.
- `not run`: deliberately omitted with a reason.

Do not write “all tests passed” when only a subset ran. A build is not a test; a test is not runtime UX validation; a mocked unit test is not a contract or migration proof.

## Test quality checks

Tests must:

- Assert business outcomes and invariants, not implementation trivia.
- Cover the original failure or drift boundary.
- Include negative, boundary, retry/idempotency, and permission cases when relevant.
- Avoid reproducing the same duplicated rule in test setup.
- Remain deterministic and isolated from production/shared mutable resources.
- Fail for the intended reason.

## Failure handling

- Diagnose the first failure before broad editing.
- Distinguish product failure, test defect, environment failure, and pre-existing failure.
- After three failed attempts based on the same hypothesis, stop, summarize the evidence, and re-plan or request the missing information.
- Never disable or weaken a valid test merely to obtain a green result.

## Completion rule

A repair is `verified` only when the checks required by its risk class pass. Otherwise label it `partial`, `blocked`, or `failed`, preserve the exact gap, and avoid claiming completion.
