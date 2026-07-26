# Autopilot Mode

`WRITE POLICY: CONTINUOUS_WRITE`

This is the default mode for `$software-evolution` with no arguments. It must deliver the complete governance loop without requiring `init`, `audit`, `govern`, or routine `resume`, and without stopping because an arbitrary number of files, findings, cycles, batches, or checkpoints was reached.

## Zero-prerequisite startup

1. Orient to repository rules, business intent, current Git state, user-owned changes, runtime options, tests, and available specialist capabilities.
2. If `.software-evolution.yml` or the configured memory control plane is missing, execute [init.md](init.md) automatically. Create only missing governance files, build enough initial context to proceed, and continue in the same run.
3. Validate configuration with `validate_project_config.py --json`. Use `effective_config`; record `defaulted_paths` and `deprecated_paths`. Legacy quota controls are accepted for compatibility but ignored. Never turn them back into execution limits.
4. Inspect current-branch `RUN-*` ledgers before creating a new one. Record an invocation owner, optional host deadline, and ISO-8601 `last_heartbeat_at` in parseable metadata:
   - Continue a `running` ledger only when it is owned by the current invocation. Never take over another active owner.
   - Treat another owner as active when the host reports its task as live or its heartbeat is fresh under the recorded host deadline. Unknown liveness is ambiguous, not abandoned.
   - Never create or adopt a new run whose branch/scope overlaps another active owner's run. An explicitly disjoint scope may proceed only after proving path and capability separation and recording the protected scope.
   - If exactly one relevant `partial` run is not actively owned and stopped because the host interrupted it or an older Skill enforced a file/cycle/window/finding/batch quota, validate drift, authority, and the last passed gate, then automatically adopt it. Recoverable partial auto-adoption does not require explicit `resume`.
   - Do not auto-adopt ambiguous, safety-blocked, authority-blocked, drift-conflicted, or failed-hypothesis runs.
5. Otherwise create a `RUN-*` ledger from [../templates/autopilot-run.md](../templates/autopilot-run.md). A host deadline may be recorded when the host actually supplies one; the Skill must not invent a shorter local deadline.
6. When inherited by `overnight`, reuse the existing Overnight ledger. Never create a nested run or reinterpret old quota fields as authority.

## Continuous autonomous cycle

Repeat until no additional safe, evidence-backed, fully verifiable work is available or a real stop condition occurs:

1. **Refresh model** — update actors, critical flows, runtime units, current diff, capabilities, invariants, known debt, incidents, and health evidence.
2. **Discover** — scan the highest-value available slice across user/business outcome, engineering/reliability, and architecture/evolution.
3. **Prove** — reproduce or triangulate candidates; reject style-only work and unsupported assumptions.
4. **Select** — choose the highest-priority repair-ready R1 or bounded R2 root cause. Record missing authority as `DEC-*` and specialist gaps as handoffs, then continue to another independent safe item.
5. **Checkpoint** — create or refresh a `BATCH-*` checkpoint before significant edits.
6. **Repair** — make the smallest coherent root-cause change. “Smallest coherent” is semantic: it may touch many files when a contract, generated surface, or cross-cutting fix legitimately requires them.
7. **Test** — add or update regression coverage and run the narrow check immediately.
8. **Verify** — run risk-required broader checks and the visible UI/API/job flow when safely runnable.
9. **Re-scan** — inspect affected callers, contracts, business rules, capability ownership, architecture fitness, runtime/release impact, and accidental churn.
10. **Remember** — update verified memory, capability, debt, health, decision, batch, and `RUN-*` evidence.
11. **Continue** — immediately select the next safe root cause. One successful repair, a large diff, or a high file count is never a stop condition.

## Checkpoint cadence, not quotas

Checkpoint after every coherent repair batch, before an expected host/context boundary, and whenever drift, authority, or environment state changes.

Record counts such as files touched, findings validated, batches completed, tests run, and elapsed time as **telemetry only**. They support review, recovery, and trend analysis; they never grant authority and never force termination.

Do not:

- Stop because `max_files_changed`, `max_total_files_changed`, `max_governance_files_changed`, `max_cycles`, `max_budget_windows`, `max_findings`, `max_scope_items`, or `max_repair_batches` was reached.
- Split a coherent root-cause repair merely to satisfy a file quota.
- Refuse a safe verified repair because it affects many callers or generated files.
- End the response or instruct the user to run `resume` after a normal batch checkpoint.

If the diff becomes broad, increase verification, compatibility analysis, rollback planning, and checkpoint detail. Control risk with evidence—not arithmetic.

## Unattended behavior

- Do not ask for confirmation for already-authorized repository-local R1/R2 work whose expected behavior, rollback, and verification are known.
- Skip and record work that needs unresolved business authority, unavailable credentials, destructive action, production mutation, deployment, migration execution, permission change, or remote publication. Continue independent safe work.
- Preserve unrelated user changes. If overlap makes one batch unsafe, choose another non-overlapping slice.
- Do not commit, push, open/merge PRs, deploy, or change external systems unless separately and explicitly authorized.
- Do not start a repair whose required verification cannot be completed with the available environment and host time. This is an evidence constraint, not a file-count constraint.

## Real stop conditions

Stop the invocation only when one of these is true:

- No additional actionable, repair-ready finding remains in the declared/searchable scope after re-scanning.
- All remaining work requires unresolved business authority, R3/R4 approval, unavailable evidence/environment, specialist capability, or protected external action.
- Drift or overlapping user work makes every available batch unsafe.
- The same repair hypothesis failed three times; quarantine that hypothesis, then continue other independent work. Stop the whole invocation only when no independent safe work remains.
- The host interrupts, rate-limits, suspends, or ends the task.

Before stopping, finish the current batch's verification as far as safely possible, update `RUN-*` and `BATCH-*`, record the exact real reason, and preserve the next safe action. A next plain `$software-evolution` invocation may automatically adopt a unique host-interrupted or legacy-quota partial after drift, authority, and last-gate validation. Use explicit `resume` only when an interruption is not safely auto-adoptable, or for drift, ambiguity, or targeted RUN/BATCH recovery.
