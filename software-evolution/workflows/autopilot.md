# Autopilot Mode

`WRITE POLICY: BUDGETED_WRITE`

This is the default mode for `$software-evolution` with no arguments. It must deliver the complete governance loop without requiring the user to run `init`, `audit`, or `govern` first.

## Zero-prerequisite startup

1. Orient to repository rules, business intent, current Git state, user-owned changes, runtime options, tests, and available specialist capabilities.
2. If `.software-evolution.yml` or the configured memory control plane is missing, execute the safe initialization procedure from [init.md](init.md) automatically. Create only missing governance files, build enough initial system/capability/verification context to proceed, and continue in the same run.
3. If the control plane exists, validate it and refresh only stale or contradicted evidence. Never demand re-initialization as a prerequisite.
4. Create a `RUN-*` ledger from [../templates/autopilot-run.md](../templates/autopilot-run.md) and load the normal budget. When this cycle is inherited by `overnight`, reuse the existing Overnight ledger and `overnight_budget`; never create a nested run or reset consumed budget. The invocation itself authorizes configured R1 and bounded R2 source/test changes, but not protected external operations.

## Autonomous cycle

Repeat this cycle while a complete repair-and-verification batch fits the remaining budget:

1. **Refresh model** — update understanding of actors, critical flows, runtime units, current diff, capabilities, invariants, known debt, incidents, and health evidence.
2. **Discover** — scan the highest-value available slice across user/business outcome, engineering/reliability, and architecture/evolution.
3. **Prove** — reproduce or triangulate candidates; reject style-only work and unproven assumptions.
4. **Select** — choose the highest-priority repair-ready R1 or bounded R2 root cause. Record blocked authority as `DEC-*` and specialist gaps as handoffs, then continue to another safe item instead of asking broad questions.
5. **Checkpoint** — create a `BATCH-*` checkpoint before significant edits.
6. **Repair** — make the smallest coherent root-cause change and add or update regression coverage.
7. **Verify** — run targeted checks, risk-required broader checks, and the visible UI/API/job flow when safely runnable.
8. **Re-scan** — inspect affected callers, contracts, business rules, capability ownership, architecture fitness, runtime/release impact, and accidental churn.
9. **Remember** — update verified memory, capability, debt, health, decision, batch, and `RUN-*` evidence.
10. **Continue** — immediately select the next safe batch; do not stop merely because one repair succeeded.

## Unattended behavior

- Do not ask for confirmation for already-authorized R1/R2 source/test work whose expected behavior, rollback, and verification are known.
- Skip and record an item that needs business authority, unavailable credentials, destructive action, production mutation, deployment, migration execution, permission change, or remote publication. Continue with independent safe work.
- Preserve unrelated user changes. If overlap makes a batch unsafe, checkpoint it and choose another non-overlapping slice.
- Do not commit, push, open/merge PRs, deploy, or change external systems unless separately and explicitly authorized.
- Keep verification reserve intact. A batch that cannot be verified must not be started.

## Stop conditions

Stop only when one of these is true:

- No additional repair-ready finding exists in the declared/searchable scope.
- Remaining time, cycle, file, batch, or verification budget cannot support one full cycle.
- All remaining work is R3/R4, authority-blocked, environment-blocked, or specialist-blocked.
- Drift or overlapping user changes make continuation unsafe.
- The same repair hypothesis failed three times or the configured consecutive-failure limit is reached.
- The host interrupts, rate-limits, suspends, or ends the run.

Before stopping, verify the final working tree as far as evidence permits, update the `RUN-*` ledger and latest `BATCH-*`, state the exact stop reason, and provide the next safe command—normally `$software-evolution resume <RUN-or-BATCH-id>`.
