# Mode Contracts

Treat the mode as a capability boundary, not a stylistic preference.

## Write-policy markers

Each workflow declares one machine-readable marker:

- `WRITE POLICY: CONTROL_PLANE_ONLY`
- `WRITE POLICY: READ_ONLY`
- `WRITE POLICY: BOUNDED_WRITE`
- `WRITE POLICY: BUDGETED_WRITE`
- `WRITE POLICY: INHERITED_OR_READ_ONLY`

Resolve the marker before running commands.

## Contract matrix

| Mode | Product code/tests | Project config/memory | Recorded governance artifacts | Data/external/production | Git/remote |
|---|---|---|---|---|---|
| `autopilot` | Session-budgeted R1/R2 with rolling Windows | Auto-create/update relevant control plane, memory, run ledger, checkpoints | Yes; Governance files use a separate ledger | No production mutation | Local inspection only; commit/push only when separately requested |
| `overnight` | Time/cycle-budgeted R1/R2 | Auto-create/update control plane, `RUN-*`, memory, checkpoints | Yes | No production mutation | Prefer isolated worktree; no remote publication without separate approval |
| `init` | No | Create/update governance control-plane files only | Initialization result | Read-only; disposable isolated test state only when needed | No commit/push unless separately requested |
| `audit` | No | No | Only with `--record`/explicit request | Read-only; avoid mutating test commands | No mutation |
| `govern` | Bounded R1/R2 | Update relevant memory/checkpoint | Yes when repository convention requires | No production mutation | Local Git inspection; commit/push only when requested |
| `repair` | Targeted proven issue | Update relevant memory/checkpoint | Yes | No production mutation without approval | Commit/push only when requested |
| `verify` | No | No | Only with `--record`/explicit request | Read-only/isolation-safe verification | No mutation |
| `deep` | Budgeted waves | Update memory/checkpoints | Yes | No production mutation without approval | Commit/push only when requested |
| `release-check` | No | No | Only with `--record`/explicit request | Production evidence read-only; never deploy/rollback | No mutation |
| `observe` | No | No | Only with `--record`/explicit request | Production read-only; never change alerts/flags/data | No mutation |
| `resume` | Inherit proven interrupted/targeted contract | Inherit | Inherit | Inherit, with all approvals preserved | Inherit |

## Read-only means read-only

A read-only mode must not:

- Edit source, tests, configuration, lock files, migrations, memory, or generated tracked files.
- Stage, commit, switch branches, reset, clean, push, merge, deploy, roll back, or mutate a PR/issue.
- Change databases, queues, caches, feature flags, alerts, dashboards, credentials, permissions, cloud resources, or user data.
- Run a command whose documented behavior mutates a shared environment.

It may run isolated/local checks that create only disposable ignored artifacts when that behavior is known and safe. Otherwise inspect without executing and label the gap.

`--record` grants only the mode-specific report and, when needed, a `DEC-*` decision package under configured governance directories. It requires `readonly.allow_record_persistence` not to be `false` and does not upgrade the mode to repair.

## Bounded writes

If `autonomy.allow_product_writes` is `false`, treat `autopilot`, `overnight`, `govern`, `repair`, and `deep` as read-only regardless of their normal contract.

A writable mode may edit only the declared coherent batch. `autopilot` and `overnight` may execute multiple batches, but each batch must independently satisfy the gates and update its `RUN-*` ledger. In Autopilot, Governance files are accounted separately from Implementation files; a Budget Window checkpoint continues in the same invocation while Session hard limits permit. Before the first edit, require:

- Proven problem and authoritative expected behavior.
- Known affected callers and protected boundaries.
- Risk class and mode/config authorization.
- Regression/characterization plan.
- Rollback and stop condition.
- Budget sufficient for validation.

If any condition fails, fall back to a read-only finding or decision record. A normal Window rollover does not change the write contract, create new authority, or require explicit `resume`. Default Autopilot may auto-adopt one unambiguous budget-only partial after validating drift and the original contract.

## Conflicting instructions

Apply this precedence:

1. Platform/tool/repository safety rules.
2. Explicit user approval for a protected operation.
3. Explicit selected mode.
4. Project configuration and risk policy.
5. General preference for autonomous repair.

Thus `audit this and fix anything obvious` remains read-only unless the user changes mode. Report repair-ready IDs and propose `$software-evolution repair <id>`.

## External side effects

Source-code autonomy never implies authorization to publish, deploy, migrate shared data, change permissions, modify production configuration, or alter external tracking systems. Obtain the applicable explicit approval at the point of action.
