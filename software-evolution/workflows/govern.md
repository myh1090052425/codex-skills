# Govern Mode

`WRITE POLICY: BOUNDED_WRITE`

Continuously govern the most relevant recent or high-value scope and complete safe, fully verifiable repair batches.

## Scope selection

1. Prefer user-specified scope.
2. Otherwise inspect uncommitted changes and the current branch diff against its likely base.
3. If no meaningful diff exists, select the highest-priority `ready` debt item or a critical flow with weak evidence.
4. Load configured budget; if absent, declare conservative limits before editing.

## Procedure

1. Execute the shared phases and the capability reuse gate.
2. Inspect the three pillars: user/business outcome, engineering/reliability, and architecture/evolution.
3. Route specialist risks and create decision records for unresolved authority.
4. Prove and rank findings. Ignore style preferences without user, business, operational, or evolution cost.
5. Form one coherent R1 or bounded R2 batch with expected behavior, regression plan, rollback, stop condition, and `BATCH-*` checkpoint.
6. Repair the minimum root cause, add tests, and run targeted then risk-required broader checks.
7. For visible behavior, exercise the affected UI/API/job flow when safely runnable.
8. Re-scan for duplicate capability, rule fragmentation, boundary leakage, temporary branches, observability gaps, and architecture fitness failures.
9. Update memory, health baseline, debt, decisions, and checkpoint only with verified evidence.
10. Start another batch only when remaining file/batch/verification budget can support a complete cycle.

## Default output

Return a compact governance summary using [../templates/governance-report.md](../templates/governance-report.md) when a durable report is required. Use [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md) for continuation state. Include detailed finding records for unresolved/high-risk items and exact verification results. Never turn budget exhaustion into an “all clear” claim.
