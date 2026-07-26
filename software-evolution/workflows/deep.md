# Deep Mode

`WRITE POLICY: BUDGETED_WRITE`

Perform sliced repository-wide governance without turning one run into an unbounded rewrite.

## Budget contract

Before scanning, declare:

- Scope worklist and exclusions.
- Maximum scope items and validated findings.
- Maximum repair waves and files changed.
- Verification reserve that cannot be consumed by discovery or editing.
- Areas explicitly deferred to a later batch.

Use `.software-evolution.yml` when valid. If absent, choose conservative explicit limits. Never claim repository-wide completion when only a slice was reviewed.

## Stages

### 1. Baseline and architecture

Refresh missing/stale init evidence. Map runtime units, dependencies, cycles, fan-in/out, shared mutable state, hotspots, critical capabilities, invariants, fitness functions, release path, and observability.

### 2. Experience and business flows

Exercise representative critical flows when safely runnable. Inspect discoverability, task length, forms/tables/dialogs, accessibility, and loading/empty/error/success/permission/recovery states. Trace issues to owning code, rules, and data effects.

### 3. Engineering reliability

Inspect frontend, backend, database, async work, resources, exceptions, transactions, idempotency, concurrency, timeouts, retries, cache/message consistency, logging, configuration, dependencies, performance, and cost signals. Route specialist concerns.

### 4. Capability and rule convergence

Cluster implementations by business effect. Detect duplicate capabilities and divergent state transitions, fields, enums, permissions, validators, and queries. Distinguish canonical owners, adapters, specializations, versions, and accidental duplication.

### 5. Prioritize and repair waves

Create a ranked finding/debt set. Prefer enabling repairs such as characterization tests, telemetry, seams, and compatibility adapters. Execute only small waves whose full verification fits the remaining budget. Defer broad migrations and contract breaks into `DEC-*`/`DEBT-*` plans.

### 6. Re-scan and checkpoint

After each wave, re-run affected inspections, update coverage and memory, and write a `BATCH-*` checkpoint using [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md). Stop before the next wave if verification reserve, file limit, evidence, environment, authority, or safety is insufficient.

## Completion language

Report with [../templates/governance-report.md](../templates/governance-report.md). Say `slice complete`, not `repository clean`, unless every declared repository-wide surface was actually covered with trustworthy evidence. Persist the next worklist slice for `resume`.
