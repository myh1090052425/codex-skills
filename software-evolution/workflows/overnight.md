# Overnight Mode

`WRITE POLICY: CONTINUOUS_WRITE`

Run the Autopilot loop unattended while the host remains available. Invoke with `$software-evolution overnight [scope]` manually before leaving, or use the same prompt in a Codex desktop Scheduled Task.

## Preflight

1. Read [../governance/unattended-execution.md](../governance/unattended-execution.md).
2. Prefer an isolated worktree. Never reset, clean, stash, overwrite, or switch away from user work to manufacture isolation.
3. Validate or automatically create the project control plane exactly as Autopilot does.
4. Validate configuration with `--json`; use `effective_config` and ignore every path listed in `deprecated_paths`.
5. Establish safe baseline commands and confirm they do not mutate production/shared data.
6. Create or safely adopt one schema-v3 `RUN-*` ledger with profile `overnight`, stable parent scope, three-lane coverage, invocation owner, optional host deadline, heartbeat, and real stop conditions. Bind any available Host durable goal to this Run.

## Execution

Execute the **Continuous autonomous cycle** from [autopilot.md](autopilot.md), one coherent verified batch at a time. When this mode is already dispatched from the shared startup: Do not rerun Autopilot startup. Do not create a nested run or invent local file/time/cycle quotas.

- Prefer high-confidence R1/R2 work that can be fully tested locally.
- Refresh the user/business, engineering/reliability, and architecture/evolution portfolio and recompute priorities globally after every verified batch.
- Checkpoint every batch and before likely host/context boundaries.
- Record file, finding, batch, test, and elapsed-time counts as telemetry only.
- When one item blocks, record it and continue another independent safe item.
- A broad but coherent fix may proceed when behavior, risk, rollback, and verification are known.
- Do not let repeated easy-to-test siblings starve another governance lane.
- Stop only after the Autopilot completion validator passes or a truthful blocked/interrupted status applies.

## Hard unattended boundaries

Never perform these without separate exact authorization:

- Deploy, rollback, production migration/backfill/data repair, feature-flag or alert mutation.
- Permission, credential, secret, billing, cloud-resource, or external-tracker mutation.
- Force push, history rewrite, branch deletion, merge, release publication, or destructive Git cleanup.
- Unbounded dependency upgrades, architecture rewrites, API/data-contract breaks, or R3/R4 changes.

Do not wait indefinitely for approval. Record blockers and continue safe independent work.

## Continuation and scheduled execution

A Skill cannot keep a powered-off computer or closed desktop app running. Keep the computer and Codex/ChatGPT desktop app running for local Scheduled Tasks.

If the host ends the task, record a real interruption and do not mark the Run or Host durable goal completed. Normal batch checkpoints do not require user intervention. A later plain invocation may automatically adopt one unique drift-safe host-interrupted or legacy-quota partial after authority and last-gate validation; use explicit `resume <id>` for ambiguity, drift, or targeted recovery.

Use [../templates/scheduled-overnight-task.md](../templates/scheduled-overnight-task.md) as the saved task prompt.
