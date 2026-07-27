<!-- software-evolution-run
{
  "schema_version": 3,
  "run_id": "RUN-TBD",
  "profile": "autopilot",
  "status": "running",
  "branch": "main",
  "head": "FULL_GIT_SHA",
  "scope_kind": "repository",
  "scope_paths": ["."],
  "latest_batch_id": "",
  "predecessor_run_id": "",
  "invocation_id": "INV-TBD",
  "host_deadline": "",
  "last_heartbeat_at": "ISO-8601-TBD",
  "coverage": {
    "user_business": "pending",
    "engineering_reliability": "pending",
    "architecture_evolution": "pending",
    "runtime_ux": "pending",
    "cross_lane_challenge": "pending",
    "open_repair_ready_work": true
  },
  "terminal_reason": ""
}
-->

# Autonomous Governance Run — {{RUN_ID}}

- Profile: `autopilot|overnight|deep`
- Status: `running|verification|completed|partial|blocked|failed|interrupted`
- Started / host deadline if supplied: `{{DATE_TIME}}` / `none|ISO-8601`
- Repository/branch/HEAD: `TBD`
- Run scope kind/paths and explicit exclusions: `repository|scoped` / `TBD`
- Current discovery cluster versus parent Run scope: `TBD`
- Initial worktree identity: `TBD`
- Effective config source: `explicit + bundled defaults`
- Defaulted config paths: `TBD`
- Deprecated legacy quota paths ignored: `TBD`
- Predecessor/adoption: `none|RUN-* + reason`
- Invocation owner / last heartbeat: `INV-*|host task identity` / `TBD`

## Continuity state

- Continuation rule: `continue while safe fully verifiable work exists and host is available`
- Counts are telemetry only: `yes`
- Parent Run scope remains stable across narrow batches: `yes|no + correction`
- Current coherent batch: `TBD`
- Last completed checkpoint: `TBD`

## Governance coverage matrix

| Lane | Declared surface / critical outcome | Fresh evidence since last material repair | Status | Next uncovered/counterexample target |
|---|---|---|---|---|
| User and business outcomes | TBD | TBD | `pending|covered|blocked` | TBD |
| Engineering and reliability | TBD | TBD | `pending|covered|blocked` | TBD |
| Architecture and evolution | TBD | TBD | `pending|covered|blocked` | TBD |
| Runtime UX/browser | TBD | TBD | `pending|covered|blocked|not_applicable` | TBD |

- Current defect family and strongest candidates from the other lanes: `TBD`
- Reason the selected batch outranks cross-lane alternatives: `TBD`

## Execution metrics

| Metric | Observed | Meaning |
|---|---:|---|
| Coherent repair batches completed | 0 | Audit/recovery telemetry only |
| Findings validated | 0 | Audit/recovery telemetry only |
| Implementation paths touched | 0 | Blast-radius telemetry only |
| Governance paths touched | 0 | Memory/checkpoint telemetry only |
| Verification commands/flows run | 0 | Evidence telemetry only |
| Reused unchanged verification receipts | 0 | Evidence reuse; record fingerprints |
| Elapsed host time | TBD | Observation only; not a Skill-imposed quota |

## Checkpoint ledger

Prefer concise rows in this canonical ledger. Create a standalone `BATCH-*` file only when risk, drift recovery, compatibility staging, repository policy, or handoff complexity requires it.

| Sequence | Batch ID/inline repair | Lane and root cause/capability | Risk | Change metrics | Verification/reused evidence | Outcome / continuation |
|---:|---|---|---|---|---|---|
| 1 | TBD | TBD | TBD | TBD | TBD | TBD |

## Skipped, quarantined, and blocked work

| ID/scope | Reason | Evidence/decision/handoff | Next safe action |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Aggregate verification

- Commands/flows and results: `TBD`
- Reused evidence and unchanged-input fingerprints: `TBD`
- Final diff and unrelated-change review: `TBD`
- Capability/business-rule/fitness re-scan: `TBD`
- Remaining proof gaps: `TBD`

## Completion challenge

Complete this section only after the last material repair and before any `completed` claim.

- Fresh cross-lane counterexample search outside the current module/taxonomy/test pattern: `TBD`
- Open Ready/In-progress debt and finding reconciliation: `TBD`
- Recent/unclassified change review: `TBD`
- Capability duplicate and business-rule split challenge: `TBD`
- Critical journey and runtime UX evidence/blocker: `TBD`
- Repair-ready work remaining: `yes|no + evidence`
- `validate_run_completion.py` command/result: `TBD`
- Host durable goal completion allowed: `yes only after validator OK|no`

## Stop and continuation

- Real terminal stop reason: `safe_work_exhausted|authority_evidence_environment_blocked|protected_boundary|drift|failure_exhaustion|host_interruption|N/A`
- Legacy quota caused this stop: `must be no`
- Latest valid checkpoint: `TBD`
- Auto-adoptable by next plain invocation: `yes|no + reason`
- Explicit Resume required: `yes|no + reason`
- Next safe action: `TBD`
