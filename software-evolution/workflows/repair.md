# Repair Mode

Repair validated findings or technical-debt items, add regression coverage, and prove the repaired behavior.

## Target selection

- If the user supplies a finding/debt ID or scope, use it.
- Otherwise choose the highest-priority item in `technical-debt.md` whose status is `ready` and whose acceptance/verification criteria are concrete.
- Do not repair a `candidate`, ambiguous business rule, or high-risk item without first closing its proof or decision gaps.

## Procedure

1. Re-read the target, related memory, repository instructions, current diff, and affected code.
2. Reproduce the behavior or establish a failing/characterization test when feasible.
3. Trace the complete relevant chain: entry point → orchestration → domain rule → persistence/external side effect → user/operator feedback.
4. Define the invariant and expected behavior before editing.
5. Classify risk and use a repair plan for medium/high-risk work.
6. Apply the smallest root-cause fix. Preserve external contracts and data compatibility by default.
7. Add tests at the lowest layer that proves the rule, plus integration/UI coverage when boundary behavior changed.
8. Run targeted checks immediately, then broader checks required by the risk class.
9. Validate the real user/API/job flow when runnable.
10. Inspect the final diff and affected callers for regressions, duplicated rules, new adapters, dead code, or unhandled states.
11. Mark the debt item `verified` only when evidence satisfies its verification criteria; otherwise mark `blocked` or `partial` with the exact gap.
12. Update architecture memory and capability map if responsibility, boundaries, rules, or canonical implementations changed.

## High-risk phased repair

For data models, permissions, core domain models, external APIs, or cross-service protocols:

1. Write the current contract and compatibility constraints.
2. Create a reversible phase plan with migration, rollback, telemetry, and acceptance checks.
3. Prefer additive/backward-compatible changes, dual-read/write only when justified, feature flags, and explicit deprecation.
4. Verify each phase independently.
5. Stop before production mutation, irreversible migration, access expansion, or destructive cleanup unless the user explicitly approves it.
