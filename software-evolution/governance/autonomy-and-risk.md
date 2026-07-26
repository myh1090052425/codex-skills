# Autonomy and Risk Policy

Autonomy completes safe work; it does not create missing authority. Both the selected mode and the risk class must permit an action.

## Risk classes

| Class | Typical scope | Default handling | Minimum evidence |
|---|---|---|---|
| R0 — observational | Read-only analysis, discovery, report, memory proposal | Execute within mode | Source/runtime evidence and coverage limits |
| R1 — low | Local bug, missing state/test, isolated duplication, deterministic error handling, bounded query improvement | Repair autonomously in writable mode | Regression test plus relevant static/module checks |
| R2 — medium | Shared component/service refactor, internal contract consolidation, retry/transaction/concurrency/performance change | Plan and repair only when impact, rollback, callers, and verification are bounded | Targeted tests, affected integration/build/runtime checks, caller review |
| R3 — high | Data model/migration, permission model, core semantics, public API/event schema, cross-service protocol | Decision/staged compatibility plan first; only reversible compatible phases when explicitly in scope | Old/transitional/final contract tests, migration/release/rollback evidence |
| R4 — protected | Production mutation, deployment/rollback, destructive cleanup, credential/access change, irreversible data, force push/history rewrite | Explicit approval at action time | Operation-specific preconditions, rollback/stop plan, post-action evidence |

## Mode gate

- `audit`, `verify`, `release-check`, and `observe` remain read-only for every risk class.
- `init` may create only missing control-plane files/directories.
- `govern` and `repair` may execute R1 and bounded R2 work up to configured `autonomy.max_risk`.
- `deep` may execute the same classes only inside the declared scope and coherent, fully verifiable repair waves.
- R3 execution requires an explicit target/approved decision and a reversible compatible phase; planning alone does not authorize a write.
- `resume` inherits the proven original gate. Unknown or drifted origin falls back to read-only.

## Autonomous repair requirements

All must be true:

- Problem is confirmed, or probable with a safe test that closes the remaining gap before material edits.
- Expected outcome and business authority are unambiguous.
- Affected callers, contracts, data, permissions, and release implications are known.
- Change is reversible and preserves external compatibility or follows an approved staged transition.
- Required tests/runtime checks are available and can cover the complete declared change.
- User-owned changes and protected boundaries are isolated.
- No production/external mutation is implied.

When one condition fails, produce a finding, decision record, specialist handoff, or blocked checkpoint rather than asking a broad question or proceeding speculatively.

## Refactoring requirements

Refactor autonomously only when semantics remain unchanged, behavior is characterized, rollback is straightforward, and the result reduces total concepts/rules/paths. A shared abstraction must have proven semantic consumers or restore an existing boundary.

Do not create `Manager`, `Facade`, `Wrapper`, `Common`, `Base`, or `Utils` layers merely to hide duplication. Prefer a domain-named canonical capability; retain deliberate duplication when coupling, ownership, deployment, or consistency costs are higher.

## R3 plan contents

Record current/desired contracts, authority, consumers, compatibility window, migration/backfill, mixed-version behavior, permissions/privacy, deployment order, flags, telemetry thresholds, rollback/roll-forward, cleanup gate, and tests for old/transitional/final states.

## Always require explicit approval

Before:

- Deleting/rewriting user or shared data.
- Running shared/production migrations, backfills, reconciliation writes, deploys, or rollbacks.
- Expanding privileges, changing authentication/authorization, handling credentials, or changing sensitive-data policy.
- Publishing externally, force-pushing, rebasing shared history, deleting remote resources, or mutating external issue/PR state unless specifically requested.
- Changing feature flags, alerts, dashboards, production config, sampling, or safety controls.
- Disabling tests, audit logging, security controls, or safeguards to obtain a green result.

## Existing changes and repeated failure

Treat uncommitted files as potentially user-owned. Preserve unrelated hunks and never use destructive reset/clean/checkout operations. After three failed attempts, quarantine that repair hypothesis, summarize evidence, question the model, and re-plan it before another edit. Continue other independent safe work; one exhausted hypothesis does not end the whole governance run.
