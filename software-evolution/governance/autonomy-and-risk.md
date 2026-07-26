# Autonomy and Risk Policy

Use autonomy to complete safe work, not to bypass uncertainty or protected boundaries.

## Risk classes

| Class | Typical changes | Default action | Minimum verification |
|---|---|---|---|
| R0 — observational | Read-only analysis, memory correction, test discovery | Execute | Source/runtime evidence |
| R1 — low | Local bug fix, error message, missing state, isolated duplication, test addition, safe query/index suggestion without production mutation | Repair autonomously | Targeted regression test plus relevant static checks |
| R2 — medium | Shared component/service refactor, transaction/retry change, performance optimization, internal contract consolidation | Plan, then repair autonomously only when impact and rollback are bounded | Targeted tests, affected integration/build checks, caller review |
| R3 — high | Data model/migration, permission model, core domain semantics, public API, event schema, cross-service protocol | Write staged plan first; execute only reversible backward-compatible phases when explicitly in scope and fully testable | Contract/migration tests, integration/end-to-end checks, rollback evidence |
| R4 — protected | Production mutation, destructive cleanup, credential/access change, irreversible data operation, force push/history rewrite | Require explicit user approval | User-approved operation-specific checks |

## Autonomous repair requirements

Repair without asking only when all are true:

- The problem is confirmed or strongly proven.
- The expected behavior is unambiguous.
- The affected scope and callers are known.
- The change is reversible and preserves contracts.
- Relevant tests can be added or run.
- No production, credential, irreversible data, or user-owned change is at risk.

## Refactoring requirements

Refactor autonomously only when:

- Business semantics remain unchanged.
- The target abstraction already has at least two proven semantic consumers, or the refactor restores an existing boundary.
- Tests characterize the affected behavior.
- The migration can be completed in one coherent batch or through compatible phases.
- The result reduces total concepts, paths, or duplicated rules rather than moving complexity.

Do not create `Manager`, `Facade`, `Wrapper`, `Common`, `Base`, or `Utils` layers merely to hide duplication. Prefer a domain-named canonical capability or keep deliberate duplication when coupling would cost more.

## High-risk plan contents

Before R3 work, record:

- Current and desired contracts.
- Business owner or authoritative rule source.
- Consumers and compatibility window.
- Data migration/backfill and rollback.
- Permission and privacy impact.
- Deployment ordering and feature flags.
- Observability and success/failure thresholds.
- Tests for old, transitional, and final states.

## Always pause for approval

Pause before:

- Deleting or rewriting user data.
- Running migrations against shared/production environments.
- Expanding privileges, changing authentication policy, or handling credentials.
- Publishing, deploying, force-pushing, rebasing shared history, or deleting remote resources.
- Disabling tests, security controls, audit logging, or data safeguards to make validation pass.

## Existing changes

- Treat uncommitted files as potentially user-owned.
- Edit them only when required for the target and preserve unrelated hunks.
- Never use destructive reset/clean/checkout commands to simplify the workspace.
- Do not commit unless the user or repository workflow requires it.
