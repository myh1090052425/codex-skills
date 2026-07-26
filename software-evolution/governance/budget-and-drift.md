# Budget and Drift Control

Bound work so every started repair can finish its verification and be safely resumed.

## Project configuration

Use `.software-evolution.yml` when present and valid. Validate it with `scripts/validate_project_config.py`. Configuration narrows autonomy; it never overrides platform, repository, risk, or approval rules.

Core controls:

- `autonomy.max_risk`
- `budget.max_scope_items`
- `budget.max_findings`
- `budget.max_repair_batches`
- `budget.max_files_changed`
- `budget.reserve_verification_minutes`
- corresponding `deep_budget` limits
- `readonly.allow_record_persistence` (explicit `--record` is still required)
- release gates, observation defaults, specialist routing, and fitness enforcement

If configuration is absent, declare conservative limits in the response/checkpoint before editing. A zero repair-batch/file budget makes the run read-only.

## Budget accounting

Count:

- One scope item per file/module/route/capability/contract explicitly inspected.
- One validated finding when it reaches confirmed/probable-with-safe-plan.
- One repair batch per independent root cause or contract boundary.
- Every changed tracked file, including tests, docs, migrations, generated artifacts, and config.

Do not evade limits by splitting one logical file or batch into artificial sub-items. Reserve verification capacity before editing. When the reserve would be consumed, stop discovery/editing and verify or checkpoint.

## Checkpoints

Use [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md). Include parseable metadata, mode, target, branch, HEAD, worktree fingerprint/entries, scope paths, budget used/remaining, decisions/approvals, last passed gate, exact failures, and next safe action.

Create/refresh a checkpoint:

- Before significant edits.
- After each verified repair wave.
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
