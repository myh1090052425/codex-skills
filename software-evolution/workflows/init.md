# Init Mode

`WRITE POLICY: CONTROL_PLANE_ONLY`

Build a trustworthy baseline so future governance starts from accumulated engineering memory. Do not modify product code, tests, dependencies, application configuration, or data.

## Procedure

1. Run common orientation and validate existing `.software-evolution.yml` when present.
2. Run `bootstrap_project_memory.py` to create only missing governance files/directories.
3. Detect stack, workspace layout, runtime/deployment units, entry points, build system, local services, test layers, release artifacts, and observability surfaces.
4. Infer product purpose from authoritative sources in this order: product/domain docs; user-visible routes/contracts/acceptance tests; domain services/models; conservative inference marked `unverified`.
5. Map critical actors and journeys. Prefer read-only flows; if mutation is essential, use only a disposable isolated test environment and leave no durable project, shared, or external state.
6. Build the architecture model: boundaries, dependency direction, aggregates, data ownership, contracts, queues, caches, permissions, failure-sensitive paths, and architecture fitness candidates.
7. Build the capability map from routes, use cases, services, jobs, commands, events, UI actions, and important queries. Normalize synonyms by business effect.
8. Establish the health and verification baseline: exact commands, current outcomes, known failures, critical-flow signals, and SLI/SLO gaps. Do not misattribute pre-existing failures.
9. Create evidence-backed debt and decision records. Mark unknown authority rather than guessing.
10. Validate consistency among source, runtime evidence, capability map, memory, health baseline, and config.

## Required outputs

```text
.software-evolution.yml
docs/software-evolution/
├── architecture-memory.md
├── capability-map.md
├── technical-debt.md
├── health-baseline.json
├── decisions/
├── batches/
└── reports/{audit,verification,release,observation}/
```

The bootstrap script never overwrites existing files. During init, re-read and merge evidence into governance files only; preserve existing entries and concurrent user/agent changes.

## Completion criteria

- Main runtime units, critical entry points, actors, journeys, capabilities, data owners, and permission boundaries are represented.
- Verification/release/observation commands and current evidence limits are recorded.
- Unknowns and authority gaps are explicit.
- The next governance action is concrete and does not require full rediscovery.
- No product file or external state was modified.
