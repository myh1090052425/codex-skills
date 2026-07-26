# Evolution and Business Consistency Governance

Apply the selected mode contract first. In a read-only mode, use this guidance only to inspect, prove, and report; do not execute the repair, convergence, or check-creation steps.

Prevent each new requirement or AI-generated patch from becoming another permanent rule source, compatibility branch, or architecture exception.

## Post-change evolution gate

After every writable batch, ask:

- Was an existing capability searched before a new implementation was added?
- Did the change create a parallel service, endpoint, component, DTO, validator, permission rule, query, event, or utility?
- Did responsibility or data ownership move across a boundary?
- Did a temporary branch, fallback, adapter, migration path, or feature flag gain an owner and exit condition?
- Did conditional complexity increase in a core flow?
- Do tests and telemetry prove the intended outcome rather than the patch shape?
- Does the release require mixed-version behavior or migration ordering?
- Should an architecture fitness function prevent recurrence?

## Business consistency inventory

Compare repeated definitions of:

- State transitions and terminal states.
- Enums/status labels and field semantics.
- Thresholds, calculations, eligibility, validation, and defaulting.
- Authorization, tenant/data visibility, ownership, and approval.
- Pricing, risk, limits, time/date, locale, retention, and reconciliation.
- Success/failure semantics across UI, API, jobs, events, logs, and metrics.

Search source, schemas, configs, migrations, tests, analytics queries, UI copy, and operational rules. A duplicated test constant can hide the same split as duplicated production code.

## Prove a rule split

1. Identify the same business question answered in multiple places.
2. Extract each implementation's inputs, boundaries, state assumptions, output/effect, and authority.
3. Find the source of truth: domain docs, approved decision, accepted tests, canonical service, schema constraint, product behavior, or owner.
4. Trace callers, historical data, compatibility, and release implications.
5. Classify as intentional context rule, versioned/deprecated rule, accidental divergence, or unknown authority.

Unify only accidental divergence with an authoritative target. Use `DEC-*` for unknown authority.

## Convergence strategy

- Place the invariant near its domain/data owner.
- Expose one stable capability/policy interface and keep boundary formatting outside it.
- Characterize variants and replace callers incrementally.
- Add table-driven/contract tests for thresholds, transitions, permissions, and mixed versions.
- Observe runtime outcomes when the rule affects delayed/asynchronous behavior.
- Remove obsolete branches only after usage, compatibility, and rollback gates pass.
- Record the decision, historical reason, and fitness function when recurrence risk is material.

## Temporary-change control

Treat a compatibility branch, flag, adapter, fallback, or duplicated write as debt unless it has a reason, owner/source, measurable exit condition, test/telemetry for both paths, and target date/version/trigger when meaningful. Record it in the current batch checkpoint and technical-debt ledger until the exit condition is verified.
