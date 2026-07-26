<!-- software-evolution-run
{
  "schema_version": 2,
  "run_id": "RUN-TBD",
  "profile": "autopilot",
  "status": "running",
  "branch": "main",
  "head": "FULL_GIT_SHA",
  "scope_paths": ["."],
  "latest_batch_id": "",
  "predecessor_run_id": "",
  "invocation_id": "INV-TBD",
  "host_deadline": "",
  "last_heartbeat_at": "ISO-8601-TBD"
}
-->

# Autonomous Governance Run — {{RUN_ID}}

- Profile: `autopilot|overnight|deep`
- Status: `running|verification|completed|partial|blocked|failed|interrupted`
- Started / host deadline if supplied: `{{DATE_TIME}}` / `none|ISO-8601`
- Repository/branch/HEAD: `TBD`
- Initial worktree identity: `TBD`
- Scope and exclusions: `TBD`
- Effective config source: `explicit + bundled defaults`
- Defaulted config paths: `TBD`
- Deprecated legacy quota paths ignored: `TBD`
- Predecessor/adoption: `none|RUN-* + reason`
- Invocation owner / last heartbeat: `INV-*|host task identity` / `TBD`

## Continuity state

- Continuation rule: `continue while safe fully verifiable work exists and host is available`
- Counts are telemetry only: `yes`
- Current coherent batch: `TBD`
- Last completed checkpoint: `TBD`

## Execution metrics

| Metric | Observed | Meaning |
|---|---:|---|
| Coherent repair batches completed | 0 | Audit/recovery telemetry only |
| Findings validated | 0 | Audit/recovery telemetry only |
| Implementation paths touched | 0 | Blast-radius telemetry only |
| Governance paths touched | 0 | Memory/checkpoint telemetry only |
| Verification commands/flows run | 0 | Evidence telemetry only |
| Elapsed host time | TBD | Observation only; not a Skill-imposed quota |

## Checkpoint ledger

| Sequence | Batch ID | Root cause/capability | Risk | Change metrics | Verification | Outcome / continuation |
|---:|---|---|---|---|---|---|
| 1 | TBD | TBD | TBD | TBD | TBD | TBD |

## Skipped, quarantined, and blocked work

| ID/scope | Reason | Evidence/decision/handoff | Next safe action |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Aggregate verification

- Commands/flows and results: `TBD`
- Final diff and unrelated-change review: `TBD`
- Capability/business-rule/fitness re-scan: `TBD`
- Remaining proof gaps: `TBD`

## Stop and continuation

- Real terminal stop reason: `safe work exhausted|authority/evidence/environment blocked|protected boundary|drift|failure exhaustion|host interruption|N/A`
- Legacy quota caused this stop: `must be no`
- Latest valid checkpoint: `TBD`
- Auto-adoptable by next plain invocation: `yes|no + reason`
- Explicit Resume required: `yes|no + reason`
- Next safe action: `TBD`
