# Mode Contracts

Resolve the mode and its write contract before running any command that may change source, tests, configuration, memory, data, Git state, external systems, or production state.

## Write-policy markers

Each workflow declares one machine-readable marker:

- `WRITE POLICY: CONTROL_PLANE_ONLY`
- `WRITE POLICY: READ_ONLY`
- `WRITE POLICY: BOUNDED_WRITE`
- `WRITE POLICY: CONTINUOUS_WRITE`
- `WRITE POLICY: INHERITED_OR_READ_ONLY`

Resolve the marker before running commands.

## Contract matrix

| Mode | Product code/tests | Project config/memory | Recorded governance artifacts | Data/external/production | Git/remote |
|---|---|---|---|---|---|
| `autopilot` | Continuous verified R1/R2 repair while safe work exists | Auto-create/update relevant control plane, memory, run ledger, checkpoints | Yes; counts are telemetry only | No production mutation | Local inspection only; commit/push only when separately requested |
| `overnight` | Same continuous verified R1/R2 loop while host is available | Auto-create/update control plane, `RUN-*`, memory, checkpoints | Yes | No production mutation | Prefer isolated worktree; no remote publication without separate approval |
| `init` | No | Create/update governance control-plane files only | Initialization result | Read-only; disposable isolated test state only when needed | No commit/push unless separately requested |
| `audit` | No | No | Only with `--record`/explicit request | Read-only; avoid mutating test commands | No mutation |
| `govern` | Coherent R1/R2 scope | Update relevant memory/checkpoint | Yes when repository convention requires | No production mutation | Local Git inspection; commit/push only when requested |
| `repair` | Targeted proven issue | Update relevant memory/checkpoint | Yes | No production mutation without approval | Commit/push only when requested |
| `verify` | No | No | Only with `--record`/explicit request | Read-only/isolation-safe verification | No mutation |
| `deep` | Continuous scoped repair waves while safe verified work exists | Update memory/checkpoints | Yes | No production mutation without approval | Commit/push only when requested |
| `release-check` | No | No | Only with `--record`/explicit request | Production evidence read-only; never deploy/rollback | No mutation |
| `observe` | No | No | Only with `--record`/explicit request | Production read-only; never change alerts/flags/data | No mutation |
| `resume` | Inherit proven interrupted/targeted contract | Inherit | Inherit | Inherit, with approvals revalidated | Inherit |

## Read-only means read-only

A read-only mode must not:

- Edit source, tests, configuration, lock files, migrations, memory, or generated tracked files.
- Stage, commit, switch branches, reset, clean, push, merge, deploy, roll back, or mutate a PR/issue.
- Change databases, queues, caches, feature flags, alerts, dashboards, credentials, permissions, cloud resources, or user data.
- Run a command whose documented behavior mutates a shared environment.

It may run isolated/local checks that create only disposable ignored artifacts when known safe. Otherwise inspect without executing and label the gap.

`--record` grants only the mode-specific report and, when needed, a `DEC-*` decision package under configured governance directories. It does not upgrade the mode to repair.

## Writable gates

If `autonomy.allow_product_writes` is `false`, treat `autopilot`, `overnight`, `govern`, `repair`, and `deep` as read-only.

A writable batch may proceed only when it has:

- Proven problem and authoritative expected behavior.
- Known affected callers and protected boundaries.
- Risk class and mode/config authorization.
- Regression or characterization plan.
- Rollback/roll-forward and stop condition.
- Available verification capable of covering the declared risk.

File count, diff size, finding count, cycle count, or batch count is not an authorization gate. A broad coherent repair increases the required evidence and verification but does not require routine user approval merely because many files are affected.

If a gate fails, create a finding, decision, specialist handoff, or blocked checkpoint and continue other independent safe work. Default Autopilot may auto-adopt one unambiguous host-interrupted or legacy-quota partial after validating drift, authority, and the original contract.

## Conflicting instructions

Apply this precedence:

1. Platform/tool/repository safety rules.
2. Explicit user approval for a protected operation.
3. Explicit selected mode.
4. Project configuration and risk policy.
5. General preference for autonomous repair.

Thus `audit this and fix anything obvious` remains read-only unless the user changes mode.

## External side effects

Source-code autonomy never implies authorization to publish, deploy, migrate shared data, change permissions, modify production configuration, or alter external tracking systems. Obtain explicit approval at the point of action.
