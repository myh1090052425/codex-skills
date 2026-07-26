# Technical Debt and Engineering Memory

Use durable records to preserve project understanding across sessions. Keep facts, decisions, and actionable debt—not debugging diaries.

## Canonical files

Default to `docs/software-evolution/`:

- `architecture-memory.md`
- `capability-map.md`
- `technical-debt.md`

If repository rules already define equivalent durable files, update those instead and record the mapping. Do not duplicate competing sources of truth.

## Architecture memory rules

Record:

- Product/business purpose and primary actors.
- Runtime/deployment map and critical flows.
- Modules, domain boundaries, aggregate/data ownership, and dependency direction.
- External contracts, queues/events, caches, permissions, and configuration boundaries.
- Quality attributes and failure-sensitive areas.
- Key decisions, constraints, prohibited patterns, and historical reasons.
- Verification commands and last verified evidence.

Mark entries as `verified`, `inferred`, or `unknown`. Correct stale memory when source/runtime evidence changes. Do not store secrets, personal data, or transient logs.

## Capability map rules

Record one row per business capability, not per method. Keep:

- Stable capability ID and canonical business name.
- Actor intent and business outcome.
- Aggregate/data ownership.
- Entry points, callers, and current implementation.
- Inputs/outputs, invariants, authorization, and side effects.
- Reuse classification and duplicate candidates.
- Evidence and last verification date.

Preserve aliases/synonyms so future searches find existing capabilities.

## Technical-debt lifecycle

Use statuses:

- `candidate`: not sufficiently proven.
- `ready`: proven with concrete remediation and verification.
- `in_progress`: current coherent repair batch.
- `partial`: some remediation landed but acceptance criteria remain.
- `blocked`: decision, environment, dependency, or approval missing.
- `verified`: remediation and required checks passed.
- `accepted`: intentionally retained with reason and review trigger.
- `obsolete`: no longer applies, with evidence.

Priorities:

- `P0`: active severe user/data/security/availability risk.
- `P1`: incorrect core business behavior, high reliability risk, or rapidly multiplying architecture debt.
- `P2`: material UX, maintainability, performance, or consistency cost.
- `P3`: bounded cleanup or improvement with low immediate impact.

## Debt quality bar

Every `ready` debt item must include:

- Problem and root cause.
- Evidence and affected scope.
- Why it matters now.
- Proposed remediation and compatibility constraints.
- Acceptance criteria and exact verification approach.
- Dependencies/decision gaps.

Do not use the debt file as a dumping ground for vague “refactor later” notes.

## Concurrent updates

Before modifying memory:

1. Re-read the latest file.
2. Update only the relevant sections/rows using stable IDs.
3. Preserve other agents' entries and formatting where practical.
4. If the same ID has conflicting concurrent edits, record the conflict and stop instead of overwriting it.

## End-of-run update

At the end of each substantive governance batch:

- Update facts and decisions that changed.
- Add or change debt status with verification evidence.
- Update capability ownership when implementation or callers changed.
- Record the next safe action.
- Keep detailed command logs in the governance report or repository state convention, not in architecture memory.
