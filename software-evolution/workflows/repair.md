# Repair Mode

`WRITE POLICY: BOUNDED_WRITE`

Repair a validated finding, decision-approved change, or ready technical-debt item and prove the repaired behavior.

## Target gate

- Use the supplied `FIND-*`, `DEBT-*`, `DEC-*`, capability, file, flow, or failure target.
- Without a target, choose the highest-priority `ready` debt item with concrete acceptance criteria.
- Do not repair a candidate, ambiguous rule, unapproved protected change, or item whose proof has drifted.

## Procedure

1. Re-read the target, authority, related memory, config, repository rules, Git identity, current diff, and affected code.
2. Reproduce the behavior or establish characterization evidence.
3. Trace entry point → orchestration → domain rule → persistence/external effect → user/operator feedback.
4. Define invariant, callers, contracts, risk, rollback, verification coverage, and stop condition before editing.
5. Create/refresh a `BATCH-*` checkpoint with [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md). For R2/R3 planning, use [../templates/repair-plan.md](../templates/repair-plan.md); R3 requires an approved staged compatibility plan.
6. Apply the smallest root-cause fix while preserving public/data compatibility by default.
7. Add the lowest-layer regression test plus boundary/UI coverage where behavior crosses a boundary.
8. Run targeted checks immediately, then risk-required integration/contract/migration/build/runtime checks and record them with [../templates/verification-record.md](../templates/verification-record.md).
9. Inspect final diff and callers for regressions, duplicated rules, dead paths, missing telemetry, or new adapters.
10. Mark the target `verified` only when acceptance evidence passes; otherwise mark `partial`, `failed`, or `blocked` with the exact gap.
11. Update memory/capability/health/checkpoint records when ownership, rules, runtime facts, or next safe action changed.

## High-risk phases

For data models, permissions, core domain semantics, public APIs, events, or cross-service protocols:

1. Record current/desired contracts and consumers.
2. Define additive transition, mixed-version behavior, migration/backfill, telemetry, rollback, and cleanup gate.
3. Verify old, transitional, and final states independently.
4. Stop before production mutation, destructive cleanup, privilege change, or irreversible migration unless explicitly approved.
