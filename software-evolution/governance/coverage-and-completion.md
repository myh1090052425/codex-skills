# Governance Coverage and Completion Proof

Prevent a continuous run from mistaking depth in one convenient defect family for ownership of the whole system. This is a semantic coverage gate, never a file/finding/cycle/time quota.

## Three core governance lanes

Every unscoped `autopilot`, `overnight`, or repository-wide `deep` run maintains a live candidate portfolio across:

1. **User and business outcomes** — critical journeys, discoverability, feedback/recovery, permissions, business correctness, and runtime experience.
2. **Engineering and reliability** — frontend/backend/data correctness, failures, concurrency, resources, performance, tests, observability, and operability.
3. **Architecture and evolution** — capability ownership/reuse, dependency direction, rule consistency, temporary complexity, fitness functions, and changeability.

Testing, release, observability, debt, and memory are cross-cutting evidence; they do not replace any core lane.

A scoped run applies the same lanes inside its declared scope. Mark a lane `blocked` with evidence when it cannot be assessed; do not silently omit it.

## Keep run scope separate from batch scope

- With no user scope, the `RUN-*` scope is the repository/system, even though each repair batch is narrow.
- A `BATCH-*` may focus on one root cause or contract boundary. Completing it never shrinks the parent run to that directory, taxonomy, or search query.
- Maintain the next evidence target for each lane in the parent run. After a material repair, refresh the global portfolio before selecting another batch.
- Before choosing another sibling from the current defect family, compare it with the strongest candidate from the other lanes. Continue the same family only when user/business risk, architecture multiplication, or reliability impact still ranks it highest; record that comparison.
- Do not optimize the governance program for issues that are merely easiest to unit-test, grep, or patch.

## Runtime experience gate

When a user-facing application is safely runnable and browser automation is available:

- Traverse navigation and at least one representative critical journey before a repository-wide completion claim.
- Inspect loading, empty, success, error, permission, timeout/retry, recovery, console, and network behavior relevant to the journey.
- Re-run the affected browser journey after every user-visible repair once automated checks pass.
- Capture screenshots/traces for material UX findings or record why capture was not useful.

Static source review, schema parsing, component tests, or HTTP success alone cannot mark the user/business lane or runtime UX as covered. If the application cannot be run safely, record the exact environment, credential, data, or tool blocker and continue other lanes.

## Cross-lane completion challenge

`safe work exhausted` is a strong evidence claim. Before using it, after the last material repair:

1. Re-scan all three lanes for the declared run scope, not only the current defect cluster.
2. Deliberately search for a counterexample outside the current module, taxonomy, and test pattern.
3. Reconcile open `ready`/`in_progress` findings and debt, recent/unclassified changes, capability-map duplicates, business-rule splits, critical journeys, and known health failures.
4. Confirm runtime UX evidence or an explicit blocker when a runnable user-facing surface exists.
5. Confirm there is no repair-ready item whose expected behavior, authority, rollback, and risk-required verification are available.
6. Update the Run coverage metadata and run `validate_run_completion.py` before setting the Run or any host durable goal to `completed`.

If fresh work is found immediately after a `safe work exhausted` claim without new repository/runtime/authority evidence, treat the old completion claim as invalid, reopen the run, and record the coverage hole.

## Proportional control plane

Governance artifacts support product work; they are not the product work.

- Keep the `RUN-*` ledger as the canonical sequence. Reuse existing finding, debt, decision, verification, and memory records instead of restating the same evidence.
- Create a standalone `BATCH-*` file when risk, drift recovery, multi-step compatibility, repository policy, or handoff complexity needs it. A small R1 repair may use a concise Run row plus its existing finding/debt record when that preserves complete evidence.
- Do not create a formal report merely to repeat a Run/Batch conclusion.
- Reuse a passed verification result only when command, environment, revision, inputs, affected paths, and relevant dependency fingerprints are unchanged. Record the fingerprint and reuse reason.
- Run narrow checks per repair, related/package checks per coherent wave, and repository-wide checks when blast radius, repository policy, or final aggregate acceptance requires them. Do not rerun an unchanged expensive suite after every sibling repair without a risk reason.
- Load the Skill and stable repository context once per invocation; refresh only facts that may have drifted.
- Update durable memory when facts or decisions changed, not after every search command.

These rules reduce churn without imposing numeric work limits. Evidence quality, risk, and semantic scope still determine the required depth.
