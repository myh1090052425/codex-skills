# Autopilot Mode

`WRITE POLICY: BUDGETED_WRITE`

This is the default mode for `$software-evolution` with no arguments. It must deliver the complete governance loop without requiring the user to run `init`, `audit`, or `govern` first, and without requiring `resume` between normal budget windows.

## Zero-prerequisite startup

1. Orient to repository rules, business intent, current Git state, user-owned changes, runtime options, tests, and available specialist capabilities.
2. If `.software-evolution.yml` or the configured memory control plane is missing, execute the safe initialization procedure from [init.md](init.md) automatically. Create only missing governance files, build enough initial system/capability/verification context to proceed, and continue in the same run.
3. Validate configuration with `validate_project_config.py --json`. Use only its `effective_config`; never invent temporary limits because an older project config omits newer keys. Record `defaulted_paths` in the run ledger.
4. Inspect current-branch `RUN-*` ledgers before creating a new one. Record an invocation owner (host task/thread identity when exposed, otherwise a generated `INV-*` nonce), ISO-8601 `session_deadline`, and ISO-8601 `last_heartbeat_at` in parseable metadata; refresh the heartbeat at each checkpoint:
   - Continue a `running` ledger only when it is already owned by the current invocation. Never take over another active owner.
   - Treat another owner as active when the host reports its task as live or its checkpoint heartbeat is still fresh under the recorded session deadline. If liveness cannot be proven either way, classify the run as ambiguous rather than assuming it is abandoned.
   - Never create or adopt a new run whose branch/scope overlaps another active owner's run. An explicitly disjoint scope may proceed only after proving path and capability separation and recording the protected active scope; otherwise remain read-only for that invocation.
   - If exactly one relevant `partial` run stopped **only** because of a normal budget/window accounting boundary, revalidate drift and automatically adopt it. This budget-only partial run auto-adoption does not require explicit `resume`.
   - If that legacy run's session deadline or hard limits already expired, preserve it and create a linked successor `RUN-*` with a fresh effective session budget; carry forward only verified evidence, unresolved queue, exclusions, and checkpoint identity.
   - Do not auto-adopt ambiguous runs, actively owned runs, safety-blocked runs, conflicting drift, failed hypotheses, or runs lacking a provable write contract.
5. Otherwise create a `RUN-*` ledger from [../templates/autopilot-run.md](../templates/autopilot-run.md). Load session hard limits from `effective_config.autopilot` and current-window limits from `effective_config.budget`.
6. When this cycle is inherited by `overnight`, reuse the existing Overnight ledger and `overnight_budget`; never create a nested run or reset consumed budget. The invocation authorizes configured R1 and bounded R2 repository-local changes, not protected external operations.

## Autonomous cycle

Repeat while a complete repair-and-verification batch fits both the current budget window and remaining session hard limits:

1. **Refresh model** — update actors, critical flows, runtime units, current diff, capabilities, invariants, known debt, incidents, and health evidence.
2. **Discover** — scan the highest-value available slice across user/business outcome, engineering/reliability, and architecture/evolution.
3. **Prove** — reproduce or triangulate candidates; reject style-only work and unproven assumptions.
4. **Select** — choose the highest-priority repair-ready R1 or bounded R2 root cause. Record blocked authority as `DEC-*` and specialist gaps as handoffs, then continue to another safe item instead of asking broad questions.
5. **Checkpoint** — create a `BATCH-*` checkpoint before significant edits and reserve enough Governance-file capacity for mandatory ledgers.
6. **Repair** — make the smallest coherent root-cause change and add or update regression coverage.
7. **Verify** — run targeted checks, risk-required broader checks, and the visible UI/API/job flow when safely runnable.
8. **Re-scan** — inspect affected callers, contracts, business rules, capability ownership, architecture fitness, runtime/release impact, and accidental churn.
9. **Remember** — update verified memory, capability, debt, health, decision, batch, and `RUN-*` evidence.
10. **Continue** — immediately select the next safe batch; one successful repair is never a stop condition.

## Window rollover

Treat a Budget Window as an internal checkpoint, not a user interaction boundary.

When any current-window limit is reached:

1. Stop new edits for that window.
2. Finish required checks, final diff review, re-scan, and honest outcome classification.
3. Record Implementation-file and Governance-file usage separately; Governance files never consume `budget.max_files_changed`.
4. Checkpoint the `BATCH-*`, current Window Ledger row, and parent `RUN-*`.
5. Recompute the verification floor from remaining wall-clock session time. It is not a consumable balance and must not become zero merely because verification ran.
6. If `autopilot.continue_after_budget_checkpoint` is true and session hard limits, safety, time, and repair-ready work still permit, increment `window_index`, reset only window counters, and continue in the **same invocation**.

Do not end the response or instruct the user to run `resume` for normal Window rollover while automatic continuation is enabled. If the project explicitly sets `autopilot.continue_after_budget_checkpoint: false`, record a configured Window checkpoint and stop without pretending that the Session hard limit was reached.

## Unattended behavior

- Do not ask for confirmation for already-authorized R1/R2 repository-local work whose expected behavior, rollback, and verification are known.
- Skip and record an item that needs business authority, unavailable credentials, destructive action, production mutation, deployment, migration execution, permission change, or remote publication. Continue with independent safe work.
- Preserve unrelated user changes. If overlap makes a batch unsafe, checkpoint it and choose another non-overlapping slice.
- Do not commit, push, open/merge PRs, deploy, or change external systems unless separately and explicitly authorized.
- Do not start a batch unless expected implementation time plus required verification fits before the session deadline and preserves the verification floor.

## Terminal stop conditions

A normal Window limit is not terminal. Stop the invocation only when one of these is true:

- A Session hard limit is reached: runtime, total cycles, total budget windows, total Implementation files, or consecutive failed batches.
- Project configuration explicitly disables continuation after the verified Window checkpoint.
- No additional repair-ready finding exists in the declared/searchable scope, including after searching for a smaller independent batch.
- All remaining work is R3/R4, authority-blocked, environment-blocked, specialist-blocked, or overlaps protected user work.
- Drift or overlapping user changes make continuation unsafe.
- The same repair hypothesis failed three times or the configured consecutive-failure limit is reached.
- The host interrupts, rate-limits, suspends, or ends the run.

Before terminal stop, finish aggregate verification as far as evidence permits and update the `RUN-*`/latest `BATCH-*`. Record whether the stop was a Session hard limit, safe-work exhaustion, safety block, drift, failure, or host interruption. If only a Session budget ended and safe work remains, the next plain `$software-evolution` invocation may automatically adopt the unique budget-only partial or create its linked successor. Reserve explicit `$software-evolution resume <id>` for true interruption, drift recovery, ambiguous state, or targeted RUN/BATCH recovery.
