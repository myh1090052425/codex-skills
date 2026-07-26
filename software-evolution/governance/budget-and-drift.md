# Budget and Drift Control

Bound work so every started repair can finish verification without turning an internal safety checkpoint into unnecessary user interaction.

## Effective project configuration

Use `.software-evolution.yml` when present and valid. Always validate with JSON output and operate from `effective_config`, which merges missing keys from the bundled template without overwriting explicit project values:

```bash
python3 <skill-root>/scripts/validate_project_config.py \
  --config .software-evolution.yml --json
```

Never invent ad hoc lower limits because an older project config omits newer sections. Configuration may narrow autonomy; it never overrides platform, repository, risk, or approval rules.

## Two-level Autopilot budget

Default `autopilot` has two levels:

1. **Session hard limits** from `autopilot`: runtime, total cycles, budget windows, total implementation files, consecutive failed batches, and checkpoint policy.
2. **Current window limits** from `budget`: scope items, findings, repair batches, implementation files, governance files, and verification reserve.

A budget window is an internal safety and verification boundary. When a window limit is reached and `autopilot.continue_after_budget_checkpoint` is `true`, finish verification, checkpoint the window, increment the window index, reset only window counters, and continue in the same invocation while session hard limits permit. Do not ask the user to run `resume` for normal window rollover. An explicit `false` narrows autonomy: finish and record the Window checkpoint, then stop with `configured checkpoint` rather than misreporting a Session hard limit.

`deep_budget` and `overnight_budget` remain whole-run limits unless their workflow explicitly declares windows.

## File accounting classes

Count unique paths changed by the current run. Editing the same path repeatedly in one window counts once.

### Implementation files

Count against `max_files_changed`:

- Product source and tests.
- Product/runtime configuration, schemas, migrations, lock files, build scripts, and tracked generated artifacts.
- User-facing, requirements, architecture, API, or operational documentation that is part of the product change.

### Governance files

Count separately against `max_governance_files_changed` and **never** consume `max_files_changed`:

- Files under the configured `memory_dir`, including `RUN-*`, `BATCH-*`, debt, capability, architecture, decisions, and reports.
- The current Software Evolution repository-state thread and its minimal `docs/state/README.md` index update.

Do not use the governance classification to hide product documentation, migrations, configuration, or unrelated cleanup. Keep governance writes minimal even when their separate budget remains.

## Other accounting rules

- One scope item per file/module/route/capability/contract explicitly inspected.
- One validated finding when it reaches confirmed/probable-with-safe-plan.
- One repair batch per independent root cause or contract boundary.
- One cycle per completed discover-select-repair-verify-rescan iteration.
- `autopilot.max_total_files_changed` counts unique implementation files across all windows in the invocation.

`reserve_verification_minutes` is a **time floor**, not a consumable token balance. Before starting a batch, retain enough remaining session time for narrow tests, risk-required broader checks, diff review, re-scan, memory reconciliation, and checkpointing. Record actual verification time separately. After a successful window checkpoint, re-establish the same floor from remaining session time; do not write “reserve remaining = 0” merely because verification was performed.

Do not evade limits by splitting one logical file or root cause into artificial items. A zero repair-batch, implementation-file, total-implementation-file, or Governance-file budget makes the applicable writable profile read-only because it cannot complete the mandatory repair/checkpoint contract.

## Window rollover

At any window limit:

1. Stop new edits for that window.
2. Finish all required verification and classify incomplete work honestly.
3. Re-scan capability, business-rule, architecture, runtime, and unrelated-change boundaries.
4. Update the `BATCH-*` checkpoint and current `RUN-*` window ledger.
5. If session hard limits, safety, time, and available work still permit, start the next window immediately in the same invocation.
6. Stop only when a session hard limit or another real stop condition is reached.

Before terminal stop, search for a smaller independent repair-ready batch that fits the remaining session and window budgets. Do not infer that no work fits merely because the highest-priority candidate is too large.

## Budget-only partial adoption

On default Autopilot startup, inspect current-branch/scope run ledgers. If exactly one relevant run that is not actively owned is `partial` solely because of a Window/file/reserve accounting boundary, validate its checkpoint and automatically adopt it. If its Session hard limits expired, create a linked successor and carry forward only verified evidence and remaining queue. Do not auto-adopt ambiguous, drift-conflicted, safety-blocked, authority-blocked, or failed-hypothesis runs.

Another active owner is a concurrency boundary, not a reason to create a second overlapping run. Determine liveness from host task state when available, otherwise from a fresh heartbeat within the recorded deadline. If liveness is ambiguous, do not assume abandonment. A separate run may proceed only for an explicitly disjoint branch/scope after recording protected paths and capability boundaries.

This automatic route is distinct from explicit `resume`, which remains for host interruption, drift recovery, ambiguity, or targeted RUN/BATCH continuation.

## Checkpoints

Use [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md). Include parseable metadata, mode, target, branch, HEAD, worktree fingerprint/entries, scope paths, implementation/governance accounting, window/session usage, decisions/approvals, last passed gate, exact failures, and next safe action.

Create or refresh a checkpoint:

- Before significant edits.
- After each verified repair wave.
- At every budget-window rollover.
- When a decision, environment, or approval blocks progress.
- Before ending an incomplete run.

Generate current metadata with:

```bash
python3 <skill-root>/scripts/check_checkpoint_drift.py --root "$PWD" \
  --snapshot --batch-id BATCH-... --mode repair --scope-path path/to/scope
```

## Drift classes

- `NO_DRIFT`: branch, HEAD, and worktree fingerprint match.
- `SAFE_DRIFT`: only new untracked, out-of-scope artifacts differ.
- `MATERIAL_DRIFT`: relevant assumptions changed but no direct scoped conflict is proven, such as a fast-forward HEAD or tracked out-of-scope edits.
- `CONFLICTING_DRIFT`: branch/history diverged or changed paths overlap checkpoint scope.
- `UNKNOWN`: metadata/Git evidence is missing or invalid.

Only `NO_DRIFT` and reviewed `SAFE_DRIFT` may continue directly. `MATERIAL_DRIFT` must rebuild evidence in read-only mode; `CONFLICTING_DRIFT` must stop or create a new batch.
