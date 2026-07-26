# Continuity, Metrics, and Drift Control

Keep autonomous governance continuous without weakening evidence, recovery, concurrency, or safety boundaries. File counts and batch counts are telemetry—not authority and not stop conditions.

## Effective project configuration

Validate `.software-evolution.yml` with JSON output and operate from `effective_config`:

```bash
python3 <skill-root>/scripts/validate_project_config.py \
  --config .software-evolution.yml --json
```

The Validator returns:

- `config`: the project file as supplied.
- `effective_config`: supported controls merged with bundled defaults.
- `defaulted_paths`: supported values inherited from the template.
- `deprecated_paths`: legacy quota controls accepted for compatibility but removed from effective behavior.

Legacy controls such as `max_files_changed`, `max_cycles`, `max_budget_windows`, `max_findings`, `max_repair_batches`, `budget`, `deep_budget`, and `overnight_budget` must never be used to stop or refuse work.

## Control risk semantically

A writable batch is bounded by one root cause, capability, invariant, contract boundary, or compatibility stage. Its size is determined by:

- Authoritative expected behavior.
- Known callers and affected data/runtime boundaries.
- Risk class and approval requirements.
- Reversibility and rollback/roll-forward path.
- Availability of regression and broader verification.
- Ability to preserve unrelated user work.

A coherent repair may touch one file or hundreds. A broad change requires stronger evidence and verification; it does not become unauthorized merely because its file count is high.

## Change metrics

Record unique paths touched, files by category, findings validated, batches completed, tests executed, elapsed time, and remaining proof gaps. Use these metrics to:

- Explain blast radius.
- Detect accidental churn.
- Plan verification and rollback.
- Compare governance trends over time.
- Resume safely after interruption.

Never use the metrics to manufacture a hard stop, reset authority, or force the user to issue another command.

## Checkpoints

Use [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md). Include parseable metadata, mode, target, branch, HEAD, worktree fingerprint/entries, scope paths, change metrics, decisions/approvals, last passed gate, exact failures, and next safe action.

Create or refresh a checkpoint:

- Before significant edits.
- After each verified coherent repair.
- Before an expected host/context boundary.
- When a decision, environment, ownership, or approval state changes.
- Before ending an incomplete run.

Generate current metadata with:

```bash
python3 <skill-root>/scripts/check_checkpoint_drift.py --root "$PWD" \
  --snapshot --batch-id BATCH-... --mode repair --scope-path path/to/scope
```

## Recoverable partial adoption

On default Autopilot startup, inspect current-branch/scope run ledgers. If exactly one relevant run that is not actively owned is `partial` because the host interrupted it or an older Skill stopped at a file/cycle/window/finding/batch quota, validate drift, current authority, and the last passed gate, then automatically adopt it. Preserve verified evidence and continue from the smallest safe step. Do not recreate or honor an obsolete quota.

Do not auto-adopt ambiguous, drift-conflicted, safety-blocked, authority-blocked, or failed-hypothesis runs.

## Concurrent Run ownership

Another active owner is a concurrency boundary. Determine liveness from host task state when available, otherwise from a fresh heartbeat under the recorded host deadline. If liveness is ambiguous, do not assume abandonment. A separate run may proceed only for an explicitly disjoint branch/scope after recording protected paths and capability boundaries.

## Drift classes

- `NO_DRIFT`: branch, HEAD, and worktree fingerprint match.
- `SAFE_DRIFT`: only reviewed untracked/out-of-scope artifacts differ.
- `MATERIAL_DRIFT`: relevant assumptions changed but no direct scoped conflict is proven.
- `CONFLICTING_DRIFT`: branch/history diverged or changed paths overlap checkpoint scope.
- `UNKNOWN`: metadata/Git evidence is missing or invalid.

Only `NO_DRIFT` and reviewed `SAFE_DRIFT` may continue directly. `MATERIAL_DRIFT` rebuilds evidence before writing; `CONFLICTING_DRIFT` stops the old path or creates a newly authorized non-conflicting batch.
