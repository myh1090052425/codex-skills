# Common Governance Loop

Use this loop for every mode. Resolve the write contract before any command that could alter source, configuration, data, external systems, or durable reports.

## Shared evidence phases

### 1. Orient and protect

- Locate the repository root and read applicable `AGENTS.md`, contribution guides, architecture docs, runbooks, test docs, project configuration, and software-evolution memory.
- Inspect Git branch, HEAD, status, relevant base/diff, and recent commits when Git exists.
- Identify user-owned changes, generated areas, migrations, secrets, production resources, shared environments, and protected boundaries.
- Validate `.software-evolution.yml` with `validate_project_config.py --json` and operate from `effective_config`. Record `deprecated_paths`; never restore ignored legacy quotas as execution limits.
- Record assumptions and turn material unknowns into discovery tasks.

### 2. Build the working system model

Capture only facts needed for the current scope:

- Business goal, actors, critical journeys, expected outcomes, and authoritative rule sources.
- Runtime units, modules, services, jobs, deployment units, and dependency direction.
- Domain aggregates, state machines, data ownership, consistency model, and permission boundaries.
- External contracts, queues/events, caches, feature flags, scheduled work, and failure behavior.
- Test layers, architecture fitness functions, release path, telemetry, and exact safe verification commands.

Treat engineering memory and health baselines as hypotheses. Correct stale entries when source, tests, runtime, or authoritative documentation disagree.

### 3. Declare scope and verification approach

Prefer user scope, then current changes, critical journeys, ready debt, and evidence-backed hotspots. For continuous modes, distinguish the parent Run scope from the current Batch/discovery cluster. With no explicit user scope, the parent Run remains repository/system-wide; a narrow repair must not rewrite it. Declare:

- Parent Run scope, current Batch/discovery scope, included modules/flows/contracts, and explicit exclusions.
- Target identity: working tree, branch/base, commit, PR, release, service, or observation window.
- Expected behavior, affected callers, risk class, rollback/roll-forward approach, and required verification.
- Specialist routes and environments that are unavailable or unsafe.

Do not declare arbitrary maximum files, findings, cycles, repair batches, or scope items. Do not claim repository-wide, production-wide, or release-wide coverage beyond the evidence actually gathered.

For unscoped `autopilot`/`overnight` and repository-wide `deep`, initialize the three-lane candidate portfolio from [../governance/coverage-and-completion.md](../governance/coverage-and-completion.md). Record the next evidence target for user/business outcomes, engineering/reliability, and architecture/evolution before deepening one cluster.

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

### 5. Prioritize globally

Order by user/data/security/availability harm, business correctness, reliability, architecture multiplication, UX impact, and then maintainability/cost. Break ties with confidence, blast radius, recurrence, reversibility, and verification quality.

Compare the strongest current candidate from every applicable governance lane. Before selecting another sibling from the same module/taxonomy/test pattern, record why it outranks cross-lane alternatives. Ease of grep, unit testing, or patching is not a priority signal.

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

Applies to `autopilot`, `overnight`, `govern`, `repair`, `deep`, and a safely resumed writable batch.

### 7. Form one coherent batch

- Group work by one root cause, capability, invariant, contract boundary, or compatibility stage.
- Define expected behavior, callers, tests, compatibility, rollback, stop condition, and observable blast radius.
- Do not split or reject the batch because of its file count. Split only at independently deployable/verifiable semantic boundaries.
- Create `DEC-*` first when business authority is unresolved.
- Establish or refresh a `BATCH-*` checkpoint before significant edits.

### 8. Establish a baseline

Reproduce the issue or capture characterization evidence when feasible. Run directly relevant existing checks and distinguish pre-existing failures from new work.

### 9. Repair incrementally

1. Add or identify a regression check.
2. Apply the minimum coherent root-cause fix.
3. Run the narrow check immediately.
4. Inspect the diff for accidental churn and record changed paths as telemetry.
5. Run risk-required broader checks.
6. Exercise the user/API/job flow when externally visible. If a user-facing application is safely runnable and browser automation exists, repeat the affected browser journey; component tests alone are insufficient.
7. Re-scan callers, rules, capability ownership, boundaries, and fitness functions.
8. Refresh the parent Run's three-lane candidate portfolio so the current defect family does not become the implicit Run scope.

Stop the same failed hypothesis after three attempts, record evidence, and re-plan. Continue other independent safe work. Do not begin a change when the required verification cannot be completed with the available environment and host lifecycle.

### 10. Verify and independently challenge

- Check positive, negative, boundary, retry/idempotency, permission, and compatibility behavior as applicable.
- Inspect final diff/status and unrelated changes.
- Challenge whether tests merely encode the implementation rather than the authoritative outcome.
- For R2/R3 work, verify rollback and transitional behavior.

### 11. Remember, checkpoint, and continue

- Update debt status only with evidence.
- Update capability/architecture memory when ownership, contracts, rules, or runtime facts changed.
- Update health baseline only from measured evidence.
- Persist exact verification status, change metrics, remaining work, Git identity, and next safe action.
- Keep the parent `RUN-*` ledger canonical. Reuse existing finding/debt/decision/verification records and create a standalone `BATCH-*` only when risk, drift recovery, compatibility staging, repository policy, or handoff complexity requires it.
- Reuse unchanged expensive verification only with matching command/environment/revision/input/dependency fingerprints; otherwise rerun the risk-required gate.
- In `autopilot`/`overnight`/`deep`, immediately continue with the globally highest-value safe verified batch. One successful repair, large diff, high file count, or exhaustion of the current defect family is not a stop condition.

## Stop and completion conditions

Quarantine an exhausted hypothesis without ending unrelated safe work. Never convert an incomplete batch or one exhausted taxonomy into a completion claim.

A continuous Run may use `safe_work_exhausted` only after the last material repair and the completion proof in [../governance/coverage-and-completion.md](../governance/coverage-and-completion.md):

- all three governance lanes were freshly covered or explicitly blocked for the declared parent Run scope;
- runnable user-facing surfaces have browser/runtime evidence or an exact blocker;
- a deliberate counterexample search outside the current module/taxonomy/test pattern found no repair-ready work;
- Ready/In-progress debt, findings, recent changes, capability duplicates, business-rule splits, critical journeys, and known health failures were reconciled;
- no item remains with known authority, rollback, and fully executable risk-required verification;
- the schema-v3 Run ledger passes `validate_run_completion.py`.

Use truthful `blocked`, `partial`, or `interrupted` status when evidence, environment, authority, approval, specialist capability, protected boundaries, drift, or Host lifecycle prevents completion. Do not mark a host durable goal complete until the Run completion validator passes. Preserve a checkpoint and next safe action. Use explicit `resume` only for true interruption, drift, ambiguity, or targeted recovery—not normal batch continuation.
