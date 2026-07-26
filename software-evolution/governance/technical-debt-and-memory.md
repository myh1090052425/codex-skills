# Technical Debt and Engineering Memory

Preserve durable facts, decisions, evidence, and resumable work—not debugging diaries.

## Canonical control-plane assets

Default to:

```text
.software-evolution.yml
docs/software-evolution/
├── architecture-memory.md
├── capability-map.md
├── technical-debt.md
├── health-baseline.json
├── decisions/       # DEC-*.md
├── batches/         # BATCH-*.md
├── runs/            # RUN-*.md
└── reports/
    ├── audit/
    ├── verification/
    ├── release/
    └── observation/
```

If repository rules define equivalent durable sources, map to them instead of creating competitors. Never store credentials, secrets, personal data, raw sensitive logs, or short-lived tokens.

## Stable IDs

- `CAP-*`: business capability.
- `FIND-*`: evidence-backed finding.
- `DEBT-*`: tracked remediation obligation.
- `DEC-*`: decision/authority record.
- `BATCH-*`: one repair/deep/autopilot batch checkpoint.
- `RUN-*`: parent Autopilot/Overnight execution ledger and resume identity.
- `VER-*`: independent verification.
- `REL-*`: release readiness review.
- `FIT-*`: architecture fitness function.

Reuse the canonical ID across reports and links; do not duplicate the same issue under new IDs.

## Architecture memory

Record product purpose/actors, runtime/deployment map, domains/data ownership, dependency direction, critical journeys, contracts/events/caches/flags, permissions/trust boundaries, quality attributes, release/rollback shape, telemetry, fitness functions, decisions, prohibited patterns, historical reasons, and verification commands.

Mark material entries `verified`, `inferred`, or `unknown`, with date/evidence. Correct stale memory when current evidence disagrees.

## Capability map

Record one row per business effect with aliases, actor/outcome, data owner, implementation, entry points/callers, inputs/outputs, invariants/authorization, state transition, side effects, consistency/deployment constraints, classification, reuse decision, and last evidence.

## Health baseline

Keep structured, non-secret baseline evidence for critical flows, quality gates, SLI/SLO, known failures, release/runtime identity, and observation gaps. Do not turn one sample into a permanent threshold or overwrite historical context without a new measured window.

## Technical-debt lifecycle

Statuses: `candidate`, `ready`, `in_progress`, `partial`, `blocked`, `verified`, `accepted`, `obsolete`.

Priorities:

- `P0`: active severe user/data/security/availability risk.
- `P1`: incorrect core behavior, high reliability risk, or rapidly multiplying architecture debt.
- `P2`: material UX, maintainability, performance/cost, consistency, or observability cost.
- `P3`: bounded cleanup/improvement with low immediate impact.

Every `ready` item needs root cause, evidence/scope, impact, remediation, compatibility, acceptance criteria, exact verification, and dependencies/decision gaps. Avoid vague “refactor later” entries.

## Decisions and checkpoints

- Decision records preserve authority, options, consequences, approval scope, and supersession.
- Batch checkpoints preserve target identity, mode, drift metadata, change telemetry, verification, approvals, and next safe action.
- Reports preserve detailed evidence without bloating architecture memory.

## Concurrent updates

Before writing any durable asset:

1. Re-read the latest file/index.
2. Merge only entries owned by the current governance thread using stable IDs.
3. Preserve other agents' changes and formatting where practical.
4. If the same ID conflicts, record the conflict and stop rather than overwriting.
5. In read-only modes, do not persist unless `--record`/explicitly requested.

## End-of-run update

Writable batches update only facts, decisions, debt statuses, capability ownership, health evidence, and next action supported by verification. Keep detailed command logs in the corresponding report/checkpoint/run ledger or repository state convention.
