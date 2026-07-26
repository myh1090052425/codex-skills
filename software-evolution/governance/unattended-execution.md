# Unattended Execution Governance

Enable sustained autonomous work without converting absence into unlimited authority and without turning internal metrics into arbitrary stopping quotas.

## Profiles

- `autopilot`: default no-argument continuous governance.
- `overnight`: the same continuous loop with stronger isolation and durable recovery while the host remains available.

Neither profile requires `init`, `audit`, `govern`, or routine `resume` first.

## Effective configuration

Validate `.software-evolution.yml` with JSON output and use `effective_config`. Record `deprecated_paths`; legacy file/cycle/window/finding/batch quotas are ignored and must not alter continuation.

## Authorization envelope

The invocation authorizes repository-local, reversible, evidence-backed R1 and bounded R2 source/test/control-plane edits allowed by repository rules and `autonomy`. It does not authorize production/shared-data mutation, deployment, remote publication, destructive Git operations, credentials, permissions, billing, or R3/R4 semantic changes.

## Isolation and user work

1. Prefer an isolated worktree for overnight execution.
2. In the current checkout, inspect branch, HEAD, worktree, and untracked files before editing.
3. Preserve all pre-existing user changes. Never stash, reset, clean, overwrite, or absorb them into a repair.
4. If paths overlap one candidate, skip that candidate or use a separately provided isolated worktree; continue other safe work.

## Continuous execution

- Continue selecting coherent, fully verifiable batches while safe work exists and the host remains available.
- Checkpoint after every batch and before likely host/context interruption.
- A file count, finding count, cycle count, batch count, elapsed-time metric, or checkpoint count is never a stop condition by itself.
- When one path fails repeatedly, quarantine that hypothesis and continue independent safe work.
- Never ask the user to restart the loop merely because an internal metric reached a threshold.

## Run ownership

Before creating a run, inspect relevant ledgers for the current branch/scope. Record parseable invocation owner, optional host deadline, and heartbeat metadata. Never take over a run owned by another active task or create an overlapping run. Unknown liveness is ambiguous, not abandoned. A disjoint run requires proven path and capability separation.

## Run ledger

Create `docs/software-evolution/runs/RUN-*.md` (or configured equivalent) from [../templates/autopilot-run.md](../templates/autopilot-run.md). Record:

- Profile, scope, branch/HEAD/worktree identity, owner/deadline/heartbeat, effective config source, defaults, and deprecated controls.
- Every batch, finding selected/skipped, exact verification, changed paths as telemetry, and remaining proof gaps.
- Decisions, specialist handoffs, protected-operation blockers, environment failures, and the real terminal reason.
- Whether the next plain invocation may auto-adopt or explicit `resume` is required.

## Failure policy

- Reproduce failures and separate product defects from environment/tooling failures.
- Stop the same repair hypothesis after three failed attempts, record evidence, and re-plan.
- Continue independent safe work after quarantining a failed hypothesis.
- Stop the whole run only when no independent safe work remains or the host/safety boundary ends execution.

## Real stop conditions

Stop only when:

- No repair-ready work remains after re-scan.
- Remaining work is authority-, approval-, evidence-, environment-, specialist-, or external-action blocked.
- Drift or overlap makes all available work unsafe.
- The host task is interrupted, suspended, rate-limited, or ended.

## Hard unattended boundaries

Never perform these without separate exact authorization:

- Deploy, rollback, production migration/backfill/data repair, feature-flag or alert mutation.
- Permission, credential, secret, billing, cloud-resource, or external-tracker mutation.
- Force push, history rewrite, branch deletion, merge, release publication, or destructive Git cleanup.
- Unbounded dependency upgrades, architecture rewrites, API/data-contract breaks, or R3/R4 changes.

Do not wait indefinitely for approval. Record the blocker and continue safe independent work.

## Scheduled execution

A Skill cannot keep a powered-off computer or closed desktop app running. For local Scheduled Tasks, keep the computer and Codex/ChatGPT desktop app running. Prefer an isolated worktree and review early runs before leaving the task unattended for long periods.

If the host ends the task, record a real interruption. Normal batch checkpoints never require user intervention. A later plain invocation may auto-adopt one unique drift-safe interrupted run; use explicit `resume <id>` for ambiguity, drift, or targeted recovery. Use [../templates/scheduled-overnight-task.md](../templates/scheduled-overnight-task.md) as the saved task prompt.
