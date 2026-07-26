# Release Check Mode

`WRITE POLICY: READ_ONLY`

Determine whether an exact change set is ready to release. Never deploy, roll back, change feature flags, execute migrations, or mutate production.

## Procedure

1. Identify target branch/base, commit SHA, build/artifact version, environment, intended rollout, and release window.
2. Read [../governance/release-and-migrations.md](../governance/release-and-migrations.md).
3. Verify source/artifact provenance, required CI/checks, test scope, unresolved findings, dependency/lockfile state, and generated artifacts.
4. Inspect API/event/schema compatibility, deployment ordering, mixed-version behavior, migrations/backfills, feature flags, cache/message implications, and rollback feasibility.
5. Define pre-deploy, during-deploy, and post-deploy checks with owners, success thresholds, stop conditions, and observation window.
6. Use production evidence only through approved read-only channels. Label missing access or telemetry as a gap.
7. Return [../templates/release-readiness.md](../templates/release-readiness.md).

## Prohibited behavior

Do not edit source/tests/configuration, execute a migration or backfill, change a feature flag, deploy, roll back, or mutate production/Git/remote state. A release blocker becomes a `repair` or decision handoff.

## Verdict

Use exactly one:

- `READY`
- `CONDITIONAL`
- `BLOCKED`
- `UNKNOWN`

`READY` requires all mandatory gates to have evidence. `CONDITIONAL` requires explicit conditions that can be checked before deployment. Persist only with `--record`/explicit request under `reports/release/`.
