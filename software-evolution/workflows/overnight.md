# Overnight Mode

`WRITE POLICY: BUDGETED_WRITE`

Run the Autopilot loop for a longer unattended session. Invoke with `$software-evolution overnight [scope]` manually before leaving, or use the same prompt in a Codex desktop Scheduled Task when available.

## Preflight

1. Read [../governance/unattended-execution.md](../governance/unattended-execution.md).
2. Prefer an isolated worktree. A clean dedicated branch/worktree is acceptable; never reset, clean, stash, overwrite, or switch away from user work to manufacture isolation.
3. Validate or automatically create the project control plane exactly as Autopilot does.
4. Validate configuration with `--json` and load `effective_config.overnight_budget`. Never invent a shorter local budget because an older project file omits that section.
5. Establish baseline commands and confirm they do not mutate production/shared data. Record unavailable services and credentials as exclusions.
6. Create or safely adopt one `RUN-*` ledger with profile `overnight`, start/deadline, repository identity, scope, whole-run budget, and stop conditions.

## Execution

Execute only the **Autonomous cycle** from [autopilot.md](autopilot.md), one `BATCH-*` at a time, under this Overnight profile. Do not rerun Autopilot startup, create a nested `RUN-*`, or replace `overnight_budget` with the normal Autopilot window budget.

- Prefer independent high-confidence R1/R2 work that can be fully tested locally.
- Recompute priorities after every verified batch instead of following a stale queue blindly.
- Account Implementation and Governance files separately using the same classification rules as normal Autopilot.
- Checkpoint after every batch and before any expected context/time boundary.
- When one item blocks on a decision or environment, record it and continue with another safe item.
- Treat the final configured verification window (`reserve_verification_minutes`) as a wall-clock floor. When remaining time reaches that floor, stop new edits and use the remainder for aggregate checks, final diff review, memory reconciliation, and checkpointing.
- Before ending on whole-run budget, search for a smaller independent batch that can still finish with verification.

## Hard unattended boundaries

Never perform these while the user is away unless a separate explicit authorization names the exact operation and target:

- Deploy, rollback, production migration/backfill/data repair, feature-flag or alert mutation.
- Permission, credential, secret, billing, cloud-resource, or external-tracker mutation.
- Force push, history rewrite, branch deletion, merge, release publication, or destructive Git cleanup.
- Unbounded dependency upgrades, architecture rewrites, API/data-contract breaks, or R3/R4 changes.

Do not wait indefinitely for approval. Record the blocker, skip the item, continue safe work, and stop only when the whole-run hard limit or another real stop condition is reached.

## Continuation and scheduled execution

A Skill does not keep a powered-off computer or closed desktop app running. For local Scheduled Tasks, keep the computer on and the Codex/ChatGPT desktop app running. Prefer an isolated worktree and review early runs before increasing the budget.

If the host ends an Overnight run, use explicit `resume` because that is a real interruption. If the only stop was the completed Overnight budget, a later `$software-evolution overnight` may auto-adopt the unique budget-only partial or create a linked successor after drift validation; normal per-batch checkpoints never require user intervention.

Use [../templates/scheduled-overnight-task.md](../templates/scheduled-overnight-task.md) as the saved task prompt.
