# Code Quality and Reliability Governance

Apply the selected mode contract first. In a read-only mode, use this guidance only to inspect, prove, and report; do not execute the repair, convergence, or check-creation steps.

Prefer correctness, clarity, controlled side effects, and operability over stylistic uniformity.

## Frontend

Inspect:

- Component responsibility, cohesion, ownership of server/client state, and prop/API stability.
- Duplicate business/UI capabilities versus legitimate presentation variants.
- Render loops, unstable dependencies, unnecessary recomputation, large bundles, and avoidable network waterfalls.
- Request cancellation, stale responses, optimistic update rollback, retries, deduplication, and cache invalidation.
- Form schema, cross-field validation, server error mapping, double submission, and unsaved state.
- Route guards, permission-aware rendering, deep links, refresh behavior, and unauthorized fallback.
- Type escapes, unsafe casts, nullable data, exhaustive state handling, and contract drift.
- Loading, empty, partial, error, offline, and success behavior.

Require a user-visible or operational consequence for material findings; do not report framework preference alone.

## Backend

Inspect:

- Controller/handler ownership of protocol concerns only.
- Service/use-case ownership of orchestration and transaction boundaries.
- Domain ownership of invariants and state transitions.
- Repository/data access ownership of persistence details rather than business policy.
- Validation at trust boundaries and canonical rule reuse inside the system.
- Exception mapping, error classification, retryability, logging context, and error swallowing.
- Transaction scope, nested calls, partial writes, outbox/event ordering, and rollback behavior.
- Idempotency keys, duplicate delivery, concurrent updates, locks/version checks, and race windows.
- Timeout budgets, cancellation propagation, connection pooling, resource closure, and backpressure.
- Configuration source, defaults, environment drift, secret handling, and unsafe feature toggles.

Trace findings through entry point → orchestration → domain/data side effect → response/event.

## Database and data access

Inspect with query/data evidence where feasible:

- Missing or unused indexes relative to filters, joins, ordering, and cardinality.
- Full scans, N+1 queries, repeated round trips, unnecessary columns, and unbounded reads.
- Large offset pagination, unstable ordering, and cursor suitability.
- Transaction isolation, lost updates, uniqueness enforcement, referential integrity, and soft-delete semantics.
- Duplicate data and denormalization without a consistency strategy.
- Migration compatibility, lock duration, backfill strategy, rollback, and mixed-version deployments.

Do not assert a performance problem solely from SQL appearance when a plan, data shape, benchmark, or clear complexity proof is needed. Record it as a candidate until proven.

## Stability and failure behavior

Inspect:

- Null/undefined/optional-state paths and exhaustive handling.
- File, stream, socket, HTTP, database, thread/task, subscription, timer, and listener lifecycle.
- Memory retention, unbounded queues/caches, oversized payloads, and accidental object graphs.
- Timeout, retry, circuit-breaking, fallback, jitter, retry storms, and deadline propagation.
- Cache invalidation, write ordering, stale reads, stampedes, and source-of-truth ambiguity.
- Message acknowledgement, deduplication, poison handling, ordering, replay, and dead-letter behavior.
- Error swallowing, misleading success, missing correlation IDs, sensitive logging, and insufficient operational context.

## Duplication test

Classify duplication before changing it:

- Textual duplication with different semantics: usually leave it.
- Structural duplication with stable shared semantics: consider extraction.
- Business-rule duplication: converge on a canonical rule.
- Business-capability duplication: follow the capability-signature process.
- Boundary adapters with equivalent internals: preserve adapters if protocols or ownership differ.

## Finding record requirements

For each confirmed issue, include:

- File and line range.
- Class/component/module.
- Method/function/query.
- Entry point and call chain.
- Root cause.
- Trigger and observed failure.
- User/data/operational impact.
- Repair, alternatives, and compatibility effect.
- Regression test and broader validation.
