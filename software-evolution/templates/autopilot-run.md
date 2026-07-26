<!-- software-evolution-run
{
  "schema_version": 1,
  "run_id": "RUN-TBD",
  "profile": "autopilot",
  "status": "running",
  "branch": "main",
  "head": "FULL_GIT_SHA",
  "scope_paths": ["."],
  "latest_batch_id": "",
  "window_index": 1,
  "predecessor_run_id": "",
  "invocation_id": "INV-TBD",
  "session_deadline": "ISO-8601-TBD",
  "last_heartbeat_at": "ISO-8601-TBD"
}
-->

# Autopilot Run — {{RUN_ID}}

- Profile: `autopilot|overnight`
- Status: `running|verification|completed|partial|blocked|failed|interrupted`
- Started/deadline: `{{DATE_TIME}}` / `TBD`
- Repository/branch/HEAD: `TBD`
- Initial worktree identity: `TBD`
- Scope and exclusions: `TBD`
- Effective config source: `explicit + bundled defaults`
- Defaulted config paths: `TBD`
- Predecessor/adoption: `none|RUN-* + reason`
- Invocation owner/last heartbeat: `INV-*|host task identity` / `TBD`

## Session hard budget

| Dimension | Limit | Used | Remaining |
|---|---:|---:|---:|
| Runtime minutes | TBD | TBD | TBD |
| Repair cycles | TBD | TBD | TBD |
| Budget Windows | TBD | TBD | TBD |
| Total Implementation files | TBD | TBD | TBD |
| Consecutive failed batches | TBD | TBD | TBD |

## Current Window budget

- Window index: `TBD`

| Dimension | Limit | Used | Remaining |
|---|---:|---:|---:|
| Scope items | TBD | TBD | TBD |
| Findings | TBD | TBD | TBD |
| Repair batches | TBD | TBD | TBD |
| Implementation files | TBD | TBD | TBD |
| Governance files | TBD | TBD | TBD |
| Verification floor minutes | TBD | `not consumable` | `recomputed from wall clock` |
| Actual verification minutes | N/A | TBD | N/A |

## Window ledger

| Window | Cycles/batches | Implementation files | Governance files | Verification | Rollover/terminal reason |
|---:|---|---:|---:|---|---|
| 1 | TBD | TBD | TBD | TBD | TBD |

## Batch ledger

| Cycle | Window | Batch ID | Finding/debt | Risk | Implementation/Governance files | Verification | Outcome |
|---:|---:|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Skipped and blocked work

| ID/scope | Reason | Evidence/decision/handoff | Next safe action |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Aggregate verification

- Commands/flows and results: `TBD`
- Final diff and unrelated-change review: `TBD`
- Capability/business-rule/fitness re-scan: `TBD`
- Remaining proof gaps: `TBD`

## Stop and continuation

- Current Window outcome: `continue same invocation|N/A`
- Terminal stop reason: `session hard limit|configured checkpoint|safe work exhausted|blocked|drift|failure|host interruption|N/A`
- Latest valid checkpoint: `TBD`
- Auto-adoptable by next plain invocation: `yes|no + reason`
- Explicit Resume required: `yes|no + reason`
- Next safe action: `TBD`
