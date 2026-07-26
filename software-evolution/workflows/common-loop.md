# Common Governance Loop

Use this loop for every mode. Resolve the write contract before any command that could alter source, configuration, data, external systems, or durable reports.

## Shared evidence phases

### 1. Orient and protect

- Locate the repository root and read applicable `AGENTS.md`, contribution guides, architecture docs, runbooks, test docs, project configuration, and software-evolution memory.
- Inspect Git branch, HEAD, status, relevant base/diff, and recent commits when Git exists.
- Identify user-owned changes, generated areas, migrations, secrets, production resources, shared environments, and protected boundaries.
- Validate `.software-evolution.yml` when present. Use conservative defaults when absent and state them.
- Record assumptions and turn material unknowns into discovery tasks.

### 2. Build the working system model

Capture only facts needed for the current scope:

- Business goal, actors, critical journeys, expected outcomes, and authoritative rule sources.
- Runtime units, modules, services, jobs, deployment units, and dependency direction.
- Domain aggregates, state machines, data ownership, consistency model, and permission boundaries.
- External contracts, queues/events, caches, feature flags, scheduled work, and failure behavior.
- Test layers, architecture fitness functions, release path, telemetry, and exact safe verification commands.

Treat engineering memory and health baselines as hypotheses. Correct stale entries when source, tests, runtime, or authoritative documentation disagree.

### 3. Declare scope and budget

Prefer user scope, then current changes, critical journeys, ready debt, and evidence-backed hotspots. Declare:

- Included files/modules/flows/contracts and explicit exclusions.
- Target identity: working tree, branch/base, commit, PR, release, service, or time window.
- Maximum scope items, findings to validate, repair batches, changed files, and verification reserve.
- Specialist routes and environments that are unavailable or unsafe.

Do not claim repository-wide, production-wide, or release-wide coverage beyond the declared worklist.

### 4. Inspect and prove

Use independent evidence channels when available:

- Source and call-chain tracing.
- Tests, schemas, migrations, fixtures, and API/event contracts.
- Browser/API/job behavior and screenshots/traces.
- Logs, metrics, traces, alerts, incidents, query plans, and deployment evidence.
- Git history and decision records when they explain intent.

Classify evidence:

- `confirmed`: directly reproduced or proven.
- `probable`: strong evidence with one material gap and an explicit validation path.
- `candidate`: useful lead, not ready for repair or release blocking unless risk demands caution.

### 5. Prioritize

Order by user/data/security/availability harm, business correctness, reliability, architecture multiplication, UX impact, and then maintainability/cost. Break ties with confidence, blast radius, recurrence, reversibility, and verification quality.

### 6. Decide the route

For each material item, choose one route:

- Report as evidence-backed finding.
- Create a decision record because authority is missing.
- Route to a specialist workflow.
- Add/advance technical debt.
- Enter a writable repair batch.
- Block release or continuation pending evidence/approval.
- Accept intentionally with reason and review trigger.

## Read-only exit

Applies to `audit`, `verify`, `release-check`, `observe`, and any `resume` that cannot prove its inherited write contract.

1. Do not edit product code, tests, project configuration, memory, data, Git state, external systems, or production state.
2. Run only commands known to be observational or isolated. Do not run tests/scripts that may mutate shared data or tracked source without a safe sandbox.
3. Produce the mode-specific report/verdict in the response.
4. Persist only when the user explicitly requests it or passes `--record`; then write only the designated report/decision file after re-reading its destination.
5. If a safe fix is obvious, identify the exact `repair` target and verification plan. Do not perform it in the read-only mode.

## Writable exit

Applies to `govern`, `repair`, budgeted repair waves in `deep`, and a safely resumed writable batch.

### 7. Form one coherent batch

- Group work by one root cause, capability, or contract boundary.
- Define expected behavior, files/callers, tests, compatibility, rollback, stop condition, and budget consumption.
- Create `DEC-*` first when business authority is unresolved.
- Establish or refresh a `BATCH-*` checkpoint before significant edits.

### 8. Establish a baseline

Reproduce the issue or capture characterization evidence when feasible. Run directly relevant existing checks and distinguish pre-existing failures from new work.

### 9. Repair incrementally

1. Add or identify a regression check.
2. Apply the minimum root-cause fix.
3. Run the narrow check immediately.
4. Inspect the diff for accidental churn and budget overflow.
5. Run risk-required broader checks.
6. Exercise the user/API/job flow when externally visible.
7. Re-scan callers, rules, capability ownership, boundaries, and fitness functions.

Stop the same failed hypothesis after three attempts. Do not start another repair batch when doing so would violate file/batch limits or consume the reserved verification budget.

### 10. Verify and independently challenge

- Check positive, negative, boundary, retry/idempotency, permission, and compatibility behavior as applicable.
- Inspect final diff/status and unrelated changes.
- Challenge whether tests merely encode the implementation rather than the authoritative outcome.
- For R2/R3 work, verify rollback and transitional behavior.

### 11. Remember and checkpoint

- Update debt status only with evidence.
- Update capability/architecture memory when ownership, contracts, rules, or runtime facts changed.
- Update health baseline only from measured evidence.
- Persist the exact verification status, remaining work, Git identity, and next safe action in the batch checkpoint.

## Stop conditions

Stop safely when:

- No actionable finding remains in scope.
- Required evidence, environment, authority, or approval is unavailable.
- A protected or irreversible boundary is next.
- Drift invalidates the current checkpoint.
- The budget cannot support another complete edit-test-rescan cycle.

Never convert an incomplete batch into a completion claim. Preserve a resumable checkpoint or a read-only finding instead.
