# Autopilot Mode

`WRITE POLICY: CONTINUOUS_WRITE`

This is the default mode for `$software-evolution` with no arguments. It must deliver the complete governance loop without requiring `init`, `audit`, `govern`, or routine `resume`, and without stopping because an arbitrary number of files, findings, cycles, batches, or checkpoints was reached.

## Zero-prerequisite startup

1. Orient to repository rules, business intent, current Git state, user-owned changes, runtime options, tests, and available specialist capabilities.
2. If `.software-evolution.yml` or the configured memory control plane is missing, execute [init.md](init.md) automatically. Create only missing governance files, build enough initial context to proceed, and continue in the same run.
3. Validate configuration with `validate_project_config.py --json`. Use `effective_config`; record `defaulted_paths` and `deprecated_paths`. Legacy quota controls are accepted for compatibility but ignored. Never turn them back into execution limits.
4. Inspect current-branch `RUN-*` ledgers before creating a new one. Record an invocation owner, optional host deadline, and ISO-8601 `last_heartbeat_at` in parseable metadata:
   - Continue a `running` ledger only when it is owned by the current invocation. Never take over another active owner.
   - Treat another owner as active when the host reports its task as live or its heartbeat is fresh under the recorded host deadline. Unknown liveness is ambiguous, not abandoned.
   - Never create or adopt a new run whose branch/scope overlaps another active owner's run. An explicitly disjoint scope may proceed only after proving path and capability separation and recording the protected scope.
   - If exactly one relevant `partial` run is not actively owned and stopped because the host interrupted it or an older Skill enforced a file/cycle/window/finding/batch quota, validate drift, authority, and the last passed gate, then automatically adopt it. Recoverable partial auto-adoption does not require explicit `resume`.
   - Do not auto-adopt ambiguous, safety-blocked, authority-blocked, drift-conflicted, or failed-hypothesis runs.
5. Otherwise create a schema-v3 `RUN-*` ledger from [../templates/autopilot-run.md](../templates/autopilot-run.md). With no explicit user scope, set `scope_kind=repository` and retain `scope_paths=["."]`; later Batch scopes must not replace the parent scope. A host deadline may be recorded only when the host supplies one.
6. Initialize the three-lane candidate portfolio from [../governance/coverage-and-completion.md](../governance/coverage-and-completion.md): user/business, engineering/reliability, and architecture/evolution. Determine whether a user-facing runtime is safely runnable and what browser journey can provide current evidence.
7. When inherited by `overnight`, reuse the existing Overnight ledger. Never create a nested run or reinterpret old quota fields as authority.

## Continuous autonomous cycle

Repeat until the completion proof passes or a real interruption/blocking status applies:

1. **Refresh model** — update actors, critical flows, runtime units, current diff, capabilities, invariants, known debt, incidents, health evidence, and the next evidence target in every governance lane.
2. **Discover broadly** — generate candidates across all applicable lanes. A current directory, response type, linter pattern, or defect taxonomy is a discovery cluster, not the Run scope.
3. **Prove** — reproduce or triangulate candidates; reject style-only work and unsupported assumptions. Use browser/runtime evidence for user journeys when safely runnable.
4. **Prioritize globally** — compare the strongest candidate from every lane. Before choosing another sibling from the current cluster, record why it outranks cross-lane alternatives; ease of testing or patching is not a priority signal.
5. **Select** — choose the highest-priority repair-ready R1 or bounded R2 root cause. Record missing authority as `DEC-*` and specialist gaps as handoffs, then continue to another independent safe item.
6. **Checkpoint proportionally** — refresh the canonical `RUN-*`. Create a separate `BATCH-*` only when risk, drift recovery, compatibility staging, repository policy, or handoff complexity needs it.
7. **Repair** — make the smallest coherent root-cause change. “Smallest coherent” is semantic: it may touch many files when a contract, generated surface, or cross-cutting fix legitimately requires them.
8. **Test** — add/update regression coverage and run the narrow check immediately. Reuse a broader passed gate only when its command/environment/revision/input/dependency fingerprint is unchanged.
9. **Verify** — run risk-required related and aggregate checks. For user-visible changes in a safely runnable application, repeat the affected browser journey after automated checks pass.
10. **Re-scan affected scope** — inspect callers, contracts, business rules, capability ownership, architecture fitness, runtime/release impact, and accidental churn.
11. **Refresh breadth** — update all three lane targets and globally re-rank before selecting the next batch. Do not let successful siblings in one taxonomy starve UX/business or architecture/evolution work.
12. **Remember** — update only changed facts, capability/debt status, decisions, health evidence, verification fingerprints, and the concise Run ledger.
13. **Continue** — immediately select the next globally highest-value safe root cause. One successful repair, a large diff, or a high file count is never a stop condition. The exhaustion of the current defect family is never a stop condition either.

## Checkpoint cadence, not quotas

Checkpoint after every coherent repair batch, before an expected host/context boundary, and whenever drift, authority, or environment state changes.

Record counts such as files touched, findings validated, batches completed, tests run, and elapsed time as **telemetry only**. They support review, recovery, and trend analysis; they never grant authority and never force termination.

Do not:

- Stop because `max_files_changed`, `max_total_files_changed`, `max_governance_files_changed`, `max_cycles`, `max_budget_windows`, `max_findings`, `max_scope_items`, or `max_repair_batches` was reached.
- Split a coherent root-cause repair merely to satisfy a file quota.
- Refuse a safe verified repair because it affects many callers or generated files.
- End the response or instruct the user to run `resume` after a normal batch checkpoint.
- Create repetitive reports or rerun an unchanged expensive full-suite gate merely to make the ledger look busy.

If the diff becomes broad, increase verification, compatibility analysis, rollback planning, and checkpoint detail. Control risk with evidence—not arithmetic.

## Unattended behavior and host continuation

- Do not ask for confirmation for already-authorized repository-local R1/R2 work whose expected behavior, rollback, and verification are known.
- Skip and record work that needs unresolved business authority, unavailable credentials, destructive action, production mutation, deployment, migration execution, permission change, or remote publication. Continue independent safe work.
- Preserve unrelated user changes. If overlap makes one batch unsafe, choose another non-overlapping slice.
- Do not commit, push, open/merge PRs, deploy, or change external systems unless separately and explicitly authorized.
- Do not start a repair whose required verification cannot be completed with the available environment and host time. This is an evidence constraint, not a file-count constraint.
- When the host exposes a durable goal/continuation primitive and the invocation requests continuous or unattended governance, bind it to the active `RUN-*`. A normal checkpoint, one exhausted cluster, or one response boundary must not complete that host goal.
- If the current host task is still active and a safe recovery is known, perform it directly; never tell the user to issue a routine `resume` command on the Agent's behalf.

## Real stop conditions

Do not infer `safe work exhausted` from the current search query or taxonomy. After the last material repair, execute the Cross-lane completion challenge in [../governance/coverage-and-completion.md](../governance/coverage-and-completion.md).

A `completed` Run requires:

- user/business, engineering/reliability, and architecture/evolution coverage marked `covered` or explicitly `blocked` for the parent scope;
- browser/runtime UX marked `covered`, explicitly `blocked`, or `not_applicable` only for a proven non-user-facing scope;
- a passed fresh counterexample search outside the current module/taxonomy/test pattern;
- reconciliation of open Ready/In-progress debt/findings, recent changes, capability duplicates, business-rule splits, critical journeys, and known health failures;
- `open_repair_ready_work=false`;
- `python3 <skill-root>/scripts/validate_run_completion.py --run <RUN-file> --json` returning `OK`.

Only then set Run status and any host durable goal to `completed`. If new repair-ready work is found without new external evidence immediately after completion, reopen the Run and record the coverage failure.

Use `partial`, `blocked`, or `interrupted` instead when all remaining work is authority/evidence/environment/specialist/protected-boundary/drift blocked or the host interrupts, rate-limits, suspends, or ends the task. The same repair hypothesis failing three times quarantines that hypothesis only; continue other independent safe work.

Before ending, finish the current batch's verification as far as safely possible, update the Run/checkpoint, record the exact real reason, and preserve the next safe action. A next plain `$software-evolution` invocation may automatically adopt a unique host-interrupted or legacy-quota partial after drift, authority, and last-gate validation. Use explicit `resume` only when an interruption is not safely auto-adoptable, or for drift, ambiguity, or targeted RUN/BATCH recovery.
