# Architecture and Capability Governance

Apply the selected mode contract first. In a read-only mode, use this guidance only to inspect, prove, and report; do not execute the repair, convergence, or check-creation steps.

Protect business ownership, data ownership, dependency direction, and the system's ability to change safely. Do not equate architecture with folder aesthetics.

## Boundary review

For each affected module/runtime unit, identify:

- Owned business decisions and data.
- Public capabilities/contracts and allowed callers.
- Inbound/outbound dependencies and deployment boundaries.
- Transaction/consistency/permission boundaries.
- Failure isolation, operational ownership, and change cadence.

Flag cycles, cross-boundary writes, shared mutable state, leaked internal models, high fan-in/out, pass-through layers, and dependency direction that bypasses the owner. Prove material claims with import/dependency graphs, call paths, schemas, runtime units, or change history.

## Capability identity

Model a business capability as:

```text
actor intent
+ business outcome/state effect
+ aggregate/data owner
+ inputs/outputs
+ invariants and authorization
+ state transition
+ side effects/events
+ entry points/callers
+ consistency/deployment constraints
```

Textual similarity is only a search clue. Different code can implement the same capability; similar code can serve different capabilities.

## Semantic duplicate detection

1. Build aliases from domain terms, UI labels, routes, commands, events, tables, DTO fields, permissions, and support language.
2. Search entry points and follow each candidate to its final data/state/event effect.
3. Normalize inputs/outputs and compare boundary conditions, authorization, idempotency, validation, transaction, and failure behavior.
4. Compare callers and why each implementation exists, including history and deployment/data ownership.
5. Classify:
   - `canonical`: authoritative owner.
   - `adapter`: protocol/UI/job/event translation into the canonical owner.
   - `specialization`: explicit additional constraint with a shared invariant core.
   - `duplicate`: independently owns the same effect and rules.
   - `uncertain`: authority/evidence gap.
6. Link accidental duplicates to one finding/debt/decision rather than creating isolated cleanup tasks.

## False-positive guardrails

Do not converge merely because implementations share CRUD shape, validation syntax, field names, or a table. Keep separation when data/deployment ownership, consistency, authorization, lifecycle, regulatory context, version compatibility, or operational failure isolation materially differs.

Do not abstract when:

- No stable semantic owner exists.
- The common interface would expose unrelated options or flags.
- Callers require divergent transaction/authorization behavior.
- The coupling cost exceeds the drift risk.

## Convergence pattern

1. Select a domain-named canonical owner.
2. Put invariants and state transitions there.
3. Keep thin boundary adapters.
4. Characterize all variants and migrate callers incrementally.
5. Support mixed versions when deployment requires it.
6. Remove duplicate paths only after usage, side effects, and rollback are verified.
7. Update capability map, architecture memory, decisions, and fitness functions.

Avoid wrapper-around-wrapper, manager/facade/service pass-through chains, generic utilities with behavior flags, universal DTOs, and centralization that violates data/deployment ownership.

## New capability gate

Before introducing a service, endpoint, component, DTO, validator, permission rule, query, event, or utility, record:

- Search terms/aliases and existing candidates.
- Semantic comparison and classification.
- Reuse/extend/adapter/new decision and owner.
- Invariant/data/permission boundary.
- Tests, compatibility, telemetry, and capability-map update.

If authority is uncertain, create `DEC-*`; do not silently add a parallel implementation.

## Architecture fitness

Register executable checks for critical boundaries using [architecture-fitness.md](architecture-fitness.md). A fitness failure is evidence to investigate, not automatic permission for a broad refactor.
