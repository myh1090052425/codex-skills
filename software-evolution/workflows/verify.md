# Verify Mode

`WRITE POLICY: READ_ONLY`

Independently accept or reject an existing working-tree change, branch, commit, PR, repair batch, Autopilot/Overnight run, finding resolution, or debt closure.

## Independence rule

Do not adopt the implementer's claims as the acceptance standard. Derive expected behavior from authoritative business rules, contracts, tests, decision records, migrations, and caller expectations. Treat supplied summaries as hypotheses.

## Procedure

1. Identify the exact target: repository, branch/base, commit SHA, diff, PR, `RUN-*`, `BATCH-*`, finding/debt ID, and environment. For a run, verify every claimed batch plus aggregate checks and stop-state evidence.
2. Reconstruct intended outcome, invariants, compatibility obligations, risk class, and required evidence.
3. Inspect the actual diff and complete affected call paths, including negative and transitional behavior.
4. Confirm the change addresses the root cause rather than only the symptom.
5. Run safe isolated checks required by risk. Record commands and distinguish product, test, environment, and pre-existing failures.
6. Challenge regression tests for false confidence, implementation coupling, missing boundaries, and absent permission/retry/idempotency cases.
7. Check capability reuse, business-rule consistency, architecture fitness, rollback, migrations, telemetry, and release implications.
8. Return [../templates/verification-report.md](../templates/verification-report.md).

## Prohibited behavior

- Do not repair failures, update tests, reformat code, change memory, or stage/commit files.
- Do not persist unless `--record` or explicitly requested; then write only under `reports/verification/`.
- A failed verification must hand off concrete proof to `repair`, not silently fix itself.

## Verdict

Use exactly one:

- `VERIFIED`
- `PARTIAL`
- `FAILED`
- `BLOCKED`
- `UNKNOWN`
