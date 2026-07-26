# Deep Mode

Perform staged repository-wide governance without turning the session into an unbounded rewrite.

## Coverage contract

Define the repository-wide worklist before claiming deep coverage. Include applicable:

- User-facing applications, routes, menus, critical journeys, accessibility and feedback states.
- Public/internal APIs, background jobs, events, queues, schedulers, and external integrations.
- Domain modules, shared libraries, data access, migrations, queries, caches, and configuration.
- Test suites, CI/build tooling, deployment artifacts, observability, and failure handling.
- Capability-map and business-rule consistency across modules.

Record excluded generated, vendored, fixture, archived, or inaccessible areas.

## Staged procedure

### Stage 1: Baseline and architecture

- Run init-mode discovery if memory is missing or stale.
- Build the module/dependency map and identify cycles, boundary violations, high fan-in/out, shared mutable state, and change hotspots.
- Identify critical capabilities and business invariants before inspecting implementation detail.

### Stage 2: Experience and business flows

- Exercise representative critical flows when runnable.
- Inspect navigation, findability, task length, forms, tables, dialogs, loading/empty/error/success/permission states, and business-flow continuity.
- Trace observed issues into owning components, APIs, rules, and data effects.

### Stage 3: Engineering reliability

- Inspect frontend, backend, database, async work, resource lifecycle, errors, timeouts, retries, idempotency, transactions, concurrency, caching, logging, and configuration.
- Use tests, query plans, runtime evidence, or concrete call paths for material claims.

### Stage 4: Capability and rule convergence

- Cluster implementations by business effect.
- Detect duplicate capabilities, duplicate rules, conflicting state transitions, field semantics, enums, permissions, validators, and queries.
- Distinguish legitimate adapters or specializations from semantic duplication.

### Stage 5: Prioritization and repair waves

- Create a ranked finding set and debt backlog.
- Execute only small repair waves with complete verification.
- Prefer enabling repairs first: missing characterization tests, observability, seams, or adapters that reduce the risk of later convergence.
- Defer broad replacements, migrations, and contract breaks into staged plans.

### Stage 6: Re-scan and report

- Re-run relevant inspections after each wave.
- Update coverage, architecture memory, capability map, and debt statuses.
- Report what was covered, fixed, deferred, blocked, and not inspected.

## Deep-mode stop rules

Stop the current run rather than manufacturing repository-wide completion when:

- The worklist cannot be completed with trustworthy evidence.
- Required services or test environments are unavailable.
- A migration or business decision is needed.
- Further work would combine unrelated changes into an unsafe patch.

Persist a checkpoint and the next worklist slice for the next deep invocation.
