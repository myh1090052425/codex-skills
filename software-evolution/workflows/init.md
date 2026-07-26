# Init Mode

Build a trustworthy baseline so future governance starts from accumulated engineering memory instead of rediscovering the project.

## Scope

Initialize understanding and durable records. Do not perform broad refactoring. Repair only a clear, low-risk blocker when it prevents baseline discovery and can be fully verified.

## Procedure

1. Run the common orientation steps and initialize missing memory files.
2. Detect the primary stack, package/workspace layout, entry points, build system, local services, test layers, and deployment artifacts.
3. Infer the product's business purpose from authoritative sources in this order:
   - Product or domain documentation.
   - User-visible routes, navigation, labels, API contracts, and acceptance tests.
   - Domain models and services.
   - Conservative inference marked as `unverified`.
4. Map critical users and journeys. If the application runs, exercise representative flows in a browser or through APIs instead of relying only on source inspection.
5. Build the initial architecture map:
   - Runtime/deployment units.
   - Modules and dependency direction.
   - Domain boundaries and core aggregates.
   - Data stores, queues, caches, external systems, and permission boundaries.
   - Critical quality attributes and failure-sensitive paths.
6. Build the initial capability map:
   - Start from routes, use cases, services, jobs, commands, events, UI actions, and important queries.
   - Normalize synonyms into business-effect names.
   - Record canonical implementations, adapters, specializations, duplicate candidates, and evidence.
7. Establish the verification baseline:
   - Document setup and test commands.
   - Run the smallest representative lint/type/unit/integration/build checks that are safe locally.
   - Record failures as baseline debt; do not misattribute pre-existing failures to new work.
8. Populate `technical-debt.md` with only evidence-backed debt. Prioritize blockers, correctness, reliability, rule divergence, and architecture multiplication before cosmetic issues.
9. Validate memory consistency against source and runtime evidence.
10. Produce an initialization report with known facts, uncertainties, commands, baseline failures, top risks, and the next recommended governance batch.

## Required outputs

- `docs/software-evolution/architecture-memory.md`
- `docs/software-evolution/capability-map.md`
- `docs/software-evolution/technical-debt.md`
- A concise user-facing initialization report

## Completion criteria

Declare initialization complete only when:

- The main runtime units and critical entry points are identified.
- At least the critical user journeys and core business capabilities are represented.
- Verification commands and their current outcomes are recorded.
- Unknowns are explicitly marked rather than silently guessed.
- The next governance action is actionable without repeating the entire discovery pass.
