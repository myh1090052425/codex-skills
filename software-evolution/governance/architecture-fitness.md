# Architecture Fitness Functions

Apply the selected mode contract first. In a read-only mode, use this guidance only to inspect, prove, and report; do not execute the repair, convergence, or check-creation steps.

Convert important architecture rules into repeatable evidence so drift is detected before it becomes convention.

## Candidate fitness functions

Use only rules that protect a real business, reliability, security, deployment, or evolution constraint:

- Allowed/forbidden module dependencies and cycle checks.
- Domain/data ownership and cross-boundary write rules.
- Public API/event/schema compatibility checks.
- Migration ordering and backward-compatible deployment checks.
- One canonical owner for critical business invariants.
- Size/complexity/hotspot thresholds with an explained risk link.
- Test, build, static, performance, or reliability gates for critical paths.
- Required telemetry fields and outcome signals.
- Dependency/runtime support and artifact provenance checks.

## Registry quality bar

Record each function in architecture memory with:

- Stable ID and protected invariant.
- Scope and authoritative reason.
- Exact command/query/manual procedure.
- Expected result and failure meaning.
- Gate level: advisory, governance, merge, release, or production observation.
- Owner and exception/expiry process.
- Last result, environment, date, and evidence link.

## Design rules

- Prefer repository-native tests and tools over introducing a new framework.
- Make checks deterministic, fast enough for their gate, and actionable when failing.
- Do not encode incidental folder layout as architecture without a real constraint.
- Avoid thresholds that create churn without preventing harm.
- Version or stage rules when migrations require temporary exceptions.
- Every exception needs reason, scope, owner/source, and removal trigger.

## Governance use

- `init`: inventory existing functions and propose missing high-value candidates; do not add product checks.
- `audit`/`verify`/`release-check`: execute applicable functions read-only and report exact failures.
- Writable modes: add or repair a fitness function when it is part of the coherent batch and verification budget.
- `deep`: prioritize missing functions that would prevent repeated architecture decay.
