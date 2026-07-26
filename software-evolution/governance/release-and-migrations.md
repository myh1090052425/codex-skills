# Release and Migration Governance

Treat release readiness as evidence about an exact artifact and rollout plan, not as “tests are green.”

## Identify the release unit

Record repository, base/head, commit SHA, build run, artifact digest/version, target environment, deployment units, rollout order, feature flags, and migration set. If source and artifact identity cannot be linked, the verdict cannot be `READY`.

## Mandatory gates

### Change and quality

- Required CI, tests, static checks, build/package checks, and unresolved P0/P1 findings.
- Final diff, generated artifacts, lockfiles, dependency/runtime support, and configuration/schema changes.
- User-visible flows and operator runbooks affected by the release.

### Compatibility and mixed versions

- Backward/forward compatibility for APIs, events, schemas, caches, files, and clients.
- Behavior while old/new services, workers, mobile/web clients, or replicas coexist.
- Idempotency and retry behavior across versions.
- Feature-flag defaults, ownership, targeting, kill switch, and removal criteria.

### Database and data migration

- Expand/migrate/contract ordering where applicable.
- Lock duration, table rewrite, online/offline behavior, replication lag, backup/recovery, and capacity.
- Backfill/reconciliation strategy, resumability, duplicate handling, and invariant checks.
- Rollback truth: whether application rollback is possible after data shape or semantics change.

### Rollout and recovery

- Pre-deploy checks, canary/percentage/stage plan, success thresholds, guardrails, stop conditions, and owner.
- Rollback or roll-forward procedure tested at the appropriate level.
- Post-deploy observation window tied to business and technical SLIs.
- Incident communication and manual fallback for critical journeys.

## Verdict rules

- `READY`: every mandatory gate has target-specific evidence and no unresolved blocker.
- `CONDITIONAL`: conditions are explicit, bounded, and verifiable before deployment.
- `BLOCKED`: a known issue or missing mandatory gate makes release unsafe.
- `UNKNOWN`: target identity or evidence is insufficient to decide.

## Production boundary

Release governance is read-only. Deploying, rolling back, executing migrations/backfills, changing feature flags, modifying production configuration, or suppressing alerts requires explicit approval at action time.
