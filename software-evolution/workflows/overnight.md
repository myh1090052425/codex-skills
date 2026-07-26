# Overnight Mode

`WRITE POLICY: BUDGETED_WRITE`

Run the Autopilot loop for a longer unattended window. Invoke with `$software-evolution overnight [scope]` manually before leaving, or use the same prompt in a Codex desktop Scheduled Task when that feature is available.

## Preflight

1. Read [../governance/unattended-execution.md](../governance/unattended-execution.md).
2. Prefer an isolated worktree. A clean dedicated branch/worktree is acceptable; never reset, clean, stash, overwrite, or switch away from user work to manufacture isolation.
3. Validate or automatically create the project control plane exactly as Autopilot does.
4. Load `overnight_budget`; if missing, declare conservative finite time, cycle, batch, file, and verification limits.
5. Establish baseline commands and confirm they do not mutate production/shared data. Record unavailable services and credentials as exclusions.
6. Create a `RUN-*` ledger with profile `overnight`, start/deadline, repository identity, scope, budget, and stop conditions.

## Execution

Execute only the **Autonomous cycle** from [autopilot.md](autopilot.md), one `BATCH-*` at a time, under this Overnight profile. Do not rerun Autopilot startup, create a nested `RUN-*`, or replace `overnight_budget` with the normal budget.

- Prefer independent high-confidence R1/R2 work that can be fully tested locally.
- Recompute priorities after every verified batch instead of following a stale queue blindly.
- Checkpoint after every batch and before any expected context/time boundary.
- When one item blocks on a decision or environment, record it and continue with another safe item.
- Reserve the final configured verification window exclusively for aggregate checks, final diff review, memory reconciliation, and a resumable checkpoint.

## Hard unattended boundaries

Never perform these while the user is away unless a separate explicit authorization names the exact operation and target:

- Deploy, rollback, production migration/backfill/data repair, feature-flag or alert mutation.
- Permission, credential, secret, billing, cloud-resource, or external-tracker mutation.
- Force push, history rewrite, branch deletion, merge, release publication, or destructive Git cleanup.
- Unbounded dependency upgrades, architecture rewrites, API/data-contract breaks, or R3/R4 changes.

Do not wait indefinitely for approval. Record the blocker, skip the item, continue safe work, and stop when no safe work remains.

## Scheduled execution reality

A Skill defines the workflow but does not keep a powered-off computer or closed desktop app running. For local Scheduled Tasks, keep the computer on and the Codex/ChatGPT desktop app running. Prefer an isolated worktree and review the first runs before increasing the budget.

Use [../templates/scheduled-overnight-task.md](../templates/scheduled-overnight-task.md) as the saved task prompt.
