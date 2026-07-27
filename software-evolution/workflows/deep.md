# Deep Mode

`WRITE POLICY: CONTINUOUS_WRITE`

Perform repository-wide or scoped deep governance through coherent, verified repair waves. Do not turn breadth into an arbitrary file/finding/batch quota.

## Coverage contract

Read [../governance/coverage-and-completion.md](../governance/coverage-and-completion.md). Before scanning, declare:

- Parent Run scope, semantic slices, and explicit exclusions.
- Critical business flows, capability boundaries, runtime units, and evidence sources.
- Verification strategy for each repair class.
- Areas blocked by authority, environment, specialist capability, or protected operations.

Never claim repository-wide completion when only a slice or one defect taxonomy was reviewed. Keep a three-lane coverage matrix and compare cross-lane candidates before deepening the same cluster. Continue to the next uncovered slice while safe verifiable work remains and the host is available.

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

Create a ranked finding/debt set. Prefer enabling repairs such as characterization tests, telemetry, seams, and compatibility adapters. Execute coherent waves whose full verification is available. Defer unresolved business semantics, destructive migrations, external writes, and R3/R4 contract changes into `DEC-*`/`DEBT-*` plans—not because of file count.

### 6. Re-scan, checkpoint, and continue

After each wave, re-run affected inspections, refresh all three lane targets, update changed memory, and checkpoint in the canonical Run ledger. Create a standalone `BATCH-*` only when risk, drift, compatibility, repository policy, or handoff complexity requires it. Record counts as coverage telemetry. Continue until the Run completion proof passes, a truthful blocking status applies, or the host ends the task.

## Completion language

Report with [../templates/governance-report.md](../templates/governance-report.md). Say `slice complete`, not `repository clean`, unless every declared repository-wide lane was covered/blocked, runtime UX evidence was acquired where applicable, the outside-cluster completion challenge passed, no repair-ready work remains, and `validate_run_completion.py` returns `OK`. Persist the next worklist slice when host interruption prevents completion.
