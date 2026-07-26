# Common Governance Loop

Use this loop for every mode. Keep each batch independently reviewable and verifiable.

## 1. Orient and protect the workspace

- Locate the repository root and read applicable `AGENTS.md`, contribution guides, architecture docs, runbooks, test docs, and existing software-evolution memory.
- Inspect `git status`, current branch, recent commits, and relevant diffs when Git exists.
- Identify user-owned uncommitted changes. Do not overwrite, revert, format, or stage unrelated files.
- Identify production resources, external services, secrets, generated files, migration directories, and other protected boundaries.
- Record assumptions. Convert important unknowns into explicit discovery tasks.

## 2. Build the working system model

Capture only facts needed for the current scope:

- Business goal, primary actors, and critical user journeys.
- Runtime entry points, modules, packages, services, jobs, and deployment units.
- Domain aggregates, state machines, core rules, and data stores.
- External contracts, queues/events, caches, feature flags, permissions, and scheduled work.
- Test layers and exact local verification commands.

Use `architecture-memory.md` as a starting hypothesis, not unquestioned truth. Correct stale entries when source or runtime evidence disagrees.

## 3. Establish the inspection scope

Prefer, in order:

1. User-specified files, flows, debt IDs, or failures.
2. Uncommitted and recently committed changes.
3. Critical business journeys and high-change modules.
4. High-priority ready items in `technical-debt.md`.
5. Risk hotspots revealed by failures, complexity, coupling, or missing coverage.

Do not claim repository-wide coverage unless the worklist actually covered the repository-wide surfaces defined in deep mode.

## 4. Discover and prove findings

Use multiple evidence channels when available:

- Static source and call-chain tracing.
- Tests, fixtures, contracts, schemas, and migrations.
- Runtime logs, API behavior, browser behavior, screenshots, and network traces.
- Git history and design decisions when they explain intentional structure.
- Data/query plans or metrics for performance claims.

Separate:

- `confirmed`: reproducible or directly proven.
- `probable`: strong evidence with one material gap.
- `candidate`: useful lead that is not ready to repair.

Only `confirmed` findings and bounded `probable` findings with a safe validation plan may enter autonomous repair.

## 5. Prioritize

Use this ordering:

1. User/data loss, security boundary break, severe outage, or blocked critical journey.
2. Incorrect business behavior or inconsistent core rules.
3. Reliability, concurrency, transaction, resource, timeout, retry, and observability failures.
4. Architecture boundary decay or duplicate business capability likely to multiply.
5. UX friction with measurable task impact.
6. Maintainability and performance debt with clear recurrence or cost.
7. Cosmetic or preference-only cleanup.

Break ties with evidence confidence, blast radius, recurrence, repair reversibility, and verification quality. Do not prioritize by how easy a finding is to describe.

## 6. Form a coherent batch

- Group changes by one root cause or one contract boundary.
- Define expected behavior, files likely to change, callers affected, tests to add, validation commands, and rollback method.
- Keep unrelated findings in `technical-debt.md` rather than mixing them into the patch.
- Establish a baseline before editing when feasible.

## 7. Repair and validate incrementally

For each batch:

1. Add or identify a failing regression check when practical.
2. Apply the minimum root-cause fix.
3. Run the narrow test immediately.
4. Inspect the diff for accidental churn.
5. Run the risk-appropriate broader validation.
6. Exercise the user/API flow when behavior is externally visible.
7. Re-scan affected callers and capability-map entries.

If the same hypothesis fails three times, stop that path and re-evaluate the model before another edit.

## 8. Persist evidence and continuation state

- Mark fixed debt items as `verified` only after their verification evidence exists.
- Add unresolved but proven work to `technical-debt.md` with a concrete next step.
- Update capability and architecture memory only with facts supported by code, tests, runtime evidence, or authoritative docs.
- Record the next safe action so another invocation can resume without rediscovery.

## 9. End-of-batch quality gate

Before ending, require all applicable answers to be explicit:

- What changed for users or operators?
- Which business capability and invariant were affected?
- Which callers, contracts, data, and modules were inspected?
- What tests would have caught the original problem?
- Which checks passed, failed, were blocked, or were not run?
- Did the change add a duplicate capability, boundary leak, temporary branch, or new debt?
- Is rollback straightforward?
