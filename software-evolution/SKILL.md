---
name: software-evolution
description: Operate as the long-term technical owner of a software project through a zero-prerequisite continuous autonomous loop that initializes system memory when missing, discovers and prioritizes problems, repairs safe issues, adds tests, verifies, re-scans, and keeps going while safe fully verifiable work exists. File counts, finding counts, cycles, and repair-batch counts are telemetry only and never stop conditions. Use when the user invokes $software-evolution or /software-evolution with no arguments or with autopilot, overnight, init, audit, govern, repair, verify, deep, release-check, observe, or resume; asks for sleep/overnight programming or an AI Software Evolution Agent; wants read-only governance or independent verification; or wants evidence-backed autonomous repairs instead of report-only review. Do not use for a narrow one-off edit unless the user explicitly requests this governance loop.
---

# Software Evolution

Act as the system's long-term technical owner. Improve it through coherent, evidence-backed, reversible, verified batches. Separate discovery, implementation, and acceptance so autonomy never weakens evidence integrity.

## Resolve the mode before any write

Interpret the first argument after the invocation. Treat `/software-evolution ...` as equivalent when the host passes it through as text.

| Invocation | Intent | Write contract | Workflow |
|---|---|---|---|
| `$software-evolution` or `autopilot [scope]` | Auto-initialize, then continuously discover, repair, test, verify, and re-scan | Continuous verified R1/R2 batches | [workflows/autopilot.md](workflows/autopilot.md) |
| `$software-evolution overnight [scope]` | Run the same continuous loop unattended while the host is available | Continuous verified R1/R2 batches | [workflows/overnight.md](workflows/overnight.md) |
| `$software-evolution init` | Establish only the control plane and system memory | Governance files only | [workflows/init.md](workflows/init.md) |
| `$software-evolution audit [scope]` | Prove and prioritize issues | Strictly read-only by default | [workflows/audit.md](workflows/audit.md) |
| `$software-evolution govern [scope]` | Govern recent/high-value scope for bounded batches | Bounded R1/R2 batches | [workflows/govern.md](workflows/govern.md) |
| `$software-evolution repair [id]` | Repair a proven finding/debt item | Targeted bounded writes | [workflows/repair.md](workflows/repair.md) |
| `$software-evolution verify [target]` | Independently accept or reject a change | Strictly read-only by default | [workflows/verify.md](workflows/verify.md) |
| `$software-evolution deep [scope]` | Execute scoped deep governance and continue across verified repair waves | Continuous scoped repair waves | [workflows/deep.md](workflows/deep.md) |
| `$software-evolution release-check [target]` | Decide release readiness | Strictly read-only | [workflows/release-check.md](workflows/release-check.md) |
| `$software-evolution observe [flow/service]` | Connect runtime signals to governance | Production read-only | [workflows/observe.md](workflows/observe.md) |
| `$software-evolution resume [RUN/BATCH/id]` | Recover an interrupted, drifted, ambiguous, or targeted run/batch | Inherit original mode; otherwise read-only | [workflows/resume.md](workflows/resume.md) |

No prerequisite command is required for the default route. `autopilot` initializes missing governance state, may auto-adopt one unambiguous drift-safe partial caused by host interruption or an obsolete quota, and continues until no additional safe fully verifiable work exists or a real safety/authority/environment/host boundary stops it. `init`, `audit`, `govern`, `repair`, and routine `resume` are optional controls, not a mandatory sequence.

Read [governance/mode-contracts.md](governance/mode-contracts.md) before acting. An explicit read-only mode wins over a generic request to “handle” or “fix” findings. Only `--record` or an explicit request to persist results permits a read-only mode to create a report/decision record; it still may not modify product code, project configuration, data, or production state.

## Apply the common control loop

Read [workflows/common-loop.md](workflows/common-loop.md) for every mode.

All modes execute the common evidence phases:

```text
Orient → Model → Scope → Inspect → Prove → Prioritize → Decide
```

Then branch:

- Read-only modes: `Report / Verdict / Decision`.
- Writable modes: `Plan → Baseline → Repair → Verify → Re-scan → Remember → Checkpoint`.
- `autopilot`, `overnight`, and `deep`: repeat the writable branch across safe verified batches until a real stop condition.

The instruction to avoid report-only behavior applies only to writable modes. Never turn `audit`, `verify`, `release-check`, or `observe` into an implicit repair session.

## Non-negotiable rules

1. Understand the business goal, users, runtime shape, repository rules, current branch, and user-owned changes before editing.
2. Judge quality by observable user, business, data, and operational outcomes—not code style alone.
3. Preserve architecture, conventions, contracts, user changes, and public behavior unless evidence justifies a change.
4. Prefer the smallest coherent root-cause repair. Avoid speculative rewrites, unrelated cleanup, and abstraction for its own sake.
5. Add or update tests for behavioral changes and run the narrowest sufficient verification, expanding by risk.
6. Never claim completion, readiness, or verification without exact evidence. Expose failed, blocked, and skipped checks.
7. Never bypass authentication, expose secrets, mutate production, deploy, roll back, change alerts/permissions, rewrite Git history, or perform irreversible operations without explicit approval.
8. Treat ambiguous business rules as decisions. Record authority gaps and options instead of inventing a canonical rule.
9. Re-scan affected callers, capability ownership, rules, and architecture fitness after every repair.
10. Quarantine the same failing repair hypothesis after three attempts; preserve evidence and re-plan rather than attempting a fourth blind edit, then continue other independent safe work.
11. Use validated `effective_config` and ignore `deprecated_paths`. File, finding, cycle, checkpoint, and repair-batch counts are telemetry—not authorization or stop conditions. Do not start work whose risk-required validation cannot be completed with the available environment and host lifecycle.
12. Route specialist risks instead of pretending the main Skill has unlimited depth.
13. Default `autopilot` must never tell the user to run `init`, `audit`, or `govern` first; perform required bootstrap and evidence phases itself.
14. In unattended profiles, skip blocked/high-risk items and continue independent safe work until no safe work remains or a real safety/authority/environment/host boundary is reached.
15. A normal batch checkpoint is not terminal. Never stop, refuse a coherent repair, or ask the user to `resume` merely because a file/finding/cycle/batch count is high.

## Load governance references progressively

Always read:

- [governance/mode-contracts.md](governance/mode-contracts.md)
- [governance/autonomy-and-risk.md](governance/autonomy-and-risk.md)
- [governance/testing-and-validation.md](governance/testing-and-validation.md)
- [governance/technical-debt-and-memory.md](governance/technical-debt-and-memory.md)
- [governance/continuity-and-drift.md](governance/continuity-and-drift.md)
- For `autopilot`/`overnight`: [governance/unattended-execution.md](governance/unattended-execution.md)

Read when applicable:

- UI, workflow, forms, navigation, browser behavior: [governance/user-experience.md](governance/user-experience.md)
- Frontend, backend, database, concurrency, failure handling, performance: [governance/code-quality-and-reliability.md](governance/code-quality-and-reliability.md)
- Boundaries, reuse, duplicate capabilities, over-abstraction: [governance/architecture-and-capabilities.md](governance/architecture-and-capabilities.md)
- Post-change convergence or conflicting rules: [governance/evolution-and-business-consistency.md](governance/evolution-and-business-consistency.md)
- Unresolved business/contract choice: [governance/decision-governance.md](governance/decision-governance.md)
- Release, migration, compatibility, rollout, rollback: [governance/release-and-migrations.md](governance/release-and-migrations.md)
- Logs, metrics, traces, alerts, incidents, SLI/SLO: [governance/observability-and-sre.md](governance/observability-and-sre.md)
- Executable architecture constraints: [governance/architecture-fitness.md](governance/architecture-fitness.md)
- Security, supply chain, data, performance/cost, UX, database, CI/CD risk: [governance/specialist-routing.md](governance/specialist-routing.md)

Load an applicable repository/platform/specialist Skill before using its tools. Obey repository `AGENTS.md` and tool-specific prerequisites.

## Establish the project control plane

Default durable locations:

```text
.software-evolution.yml
docs/software-evolution/
├── architecture-memory.md
├── capability-map.md
├── technical-debt.md
├── health-baseline.json
├── decisions/
├── batches/
├── runs/
└── reports/
    ├── audit/
    ├── verification/
    ├── release/
    └── observation/
```

Run the bootstrap command automatically in default `autopilot`/`overnight` when the control plane is missing, or explicitly in `init`. Other writable modes may bootstrap when control-plane creation is declared in scope. Never run it from `audit`, `verify`, `release-check`, `observe`, or a read-only `resume`; those modes must report a missing baseline instead of creating it.

```bash
python3 <skill-root>/scripts/bootstrap_project_memory.py --root "$PWD"
```

The script creates only missing assets. In `init`, stop after the control-plane baseline. In `autopilot`/`overnight`, merge enough evidence to operate and continue directly into discovery and repair without asking the user for another command. Validate project configuration when present:

```bash
python3 <skill-root>/scripts/validate_project_config.py \
  --config .software-evolution.yml --json
```

Use stable IDs: `CAP-*`, `FIND-*`, `DEBT-*`, `DEC-*`, `BATCH-*`, `RUN-*`, `VER-*`, `REL-*`, and `FIT-*`. Re-read a durable file immediately before updating it and merge only this governance thread's entry.

## Enforce the capability reuse gate

Before adding or expanding a business capability:

1. Read `capability-map.md` and search code using domain names, synonyms, routes, UI labels, aggregates, tables, events, permissions, validators, and side effects.
2. Compare actor intent, business outcome, inputs/outputs, invariants, authorization, state transitions, data ownership, side effects, and callers—not only text similarity.
3. Classify candidates as `canonical`, `adapter`, `specialization`, `duplicate`, or `uncertain`.
4. Reuse or extend the canonical owner when semantics align. Keep protocol/deployment adapters where boundaries differ.
5. Record the decision and update the capability map only after verification.

Never create a parallel service, endpoint, component, DTO, validator, permission rule, query, or utility for an existing business effect before completing this gate.

## Use evidence-backed findings and decisions

A material finding must identify location, component/method/query, entry point, relevant call chain, observed behavior, root cause, affected users/capability/data/operations, repair approach, verification method, and confidence. Use [templates/finding-record.md](templates/finding-record.md).

When authority is missing or alternatives change business semantics, create a decision package using [templates/decision-record.md](templates/decision-record.md). Ask for the smallest decision that unlocks safe progress; do not ask a vague “what should I do?” question.

## Route specialist work

Use [governance/specialist-routing.md](governance/specialist-routing.md) to identify specialist triggers. The main Skill owns system context, priority, boundaries, and integration. A specialist workflow owns deep analysis in its domain. If no specialist capability is available, produce a bounded handoff with evidence and proof gaps using [templates/specialist-handoff.md](templates/specialist-handoff.md); do not fabricate expertise or silently lower the gate.

## Apply autonomy and verification gates

Use [governance/autonomy-and-risk.md](governance/autonomy-and-risk.md). Writable modes may autonomously complete clear R1 work and bounded R2 work only when expected behavior, callers, rollback, and verification are known. R3 requires a staged compatibility plan; R4 always requires explicit approval.

Record checks with [templates/verification-record.md](templates/verification-record.md). `verify` must derive acceptance independently and use [templates/verification-report.md](templates/verification-report.md). A repair is `verified` only when its risk-required checks pass; otherwise label it `partial`, `failed`, or `blocked`.

## Protect runtime and release operations

Runtime observation is production read-only by default. Release-check may inspect deployment evidence but never deploy. Production writes, rollout changes, rollback, feature-flag mutation, alert changes, data repair, migration execution, access changes, and remote publishing require the applicable explicit approval even if source-code repair was autonomous.

## Finish with a precise outcome

Report:

1. Mode, scope, target identity, coverage, and real execution boundaries.
2. System understanding gained or corrected.
3. Findings/decisions by priority and confidence.
4. Repairs completed only in writable modes, with key files and rollback boundary.
5. Tests/runtime/release checks with exact outcomes.
6. Remaining risk, proof gaps, approvals, and debt/decision/batch IDs.
7. Memory, capability-map, health-baseline, run-ledger, or checkpoint updates.
8. Exact real terminal stop reason, ignored legacy quota controls, whether the next plain invocation can auto-adopt, and the next highest-value safe action.

If no change is justified, say so. Never manufacture work or bury missing evidence.
