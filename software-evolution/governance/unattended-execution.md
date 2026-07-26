# Unattended Execution Governance

Enable sustained autonomous work without converting absence into unlimited authority or turning an internal checkpoint into repeated user interaction.

## Profiles

- `autopilot`: default no-argument run; automatically initializes when needed and uses Session hard limits plus rolling Budget Windows.
- `overnight`: longer unattended run using `overnight_budget`, stronger isolation, a deadline, a verification floor, and a durable `RUN-*` ledger.

Neither profile requires the user to run `init`, `audit`, or `govern` first. Normal Budget Window rollover also does not require a routine `resume` command.

## Effective configuration

Validate `.software-evolution.yml` with JSON output and operate from `effective_config`. Missing keys in an older project file inherit bundled defaults and appear in `defaulted_paths`; they do not authorize the Agent to invent a shorter convenience budget.

## Authorization envelope

The invocation authorizes only repository-local, reversible, evidence-backed R1 and bounded R2 source/test/control-plane edits allowed by configuration and repository rules. It does not authorize production or shared-data mutation, deployment, remote publication, destructive Git operations, credentials, permissions, billing, or R3/R4 semantic changes.

## Isolation and user work

1. Prefer a Codex isolated worktree for overnight runs.
2. If running in the current checkout, inspect branch, HEAD, worktree, and untracked files before editing.
3. Preserve all pre-existing user changes. Do not stash, reset, clean, overwrite, or absorb them into a repair.
4. If changed paths overlap a candidate batch, skip/checkpoint that batch or work in a separately provided isolated worktree.

## Session and Window control

For normal Autopilot:

- Session hard limits bound total runtime, repair cycles, Budget Windows, Implementation files, and consecutive failed batches.
- Window limits bound scope, findings, repair batches, Implementation files, Governance files, and the verification floor.
- Reaching a Window limit triggers verification, ledger update, counter reset, and same-invocation continuation while Session limits permit.
- A Window rollover never requires `$software-evolution resume`.

For Overnight, `overnight_budget` is the whole-run envelope unless the project explicitly defines a future windowed profile.

## File accounting

- **Implementation files** include product source/tests/configuration/schema/migration/build/lock/generated artifacts and product-facing requirement/architecture/API/operations documents. Count them against `max_files_changed` and, for Autopilot, `max_total_files_changed`.
- **Governance files** include the configured memory directory, `RUN-*`, `BATCH-*`, debt/capability/architecture reports, the current Software Evolution state thread, and its minimal state index update. Count them only against `max_governance_files_changed`.
- Do not count the same unique path twice within the applicable Window or Session ledger. Never use Governance writes to hide product documentation or implementation changes.

## Run ownership and automatic continuation

Before creating a run, inspect relevant ledgers for the current branch/scope. Record an invocation owner and checkpoint heartbeat. Never take over a `running` ledger owned by another task or create a second run that overlaps its branch/scope. Prove liveness from host task state or a fresh heartbeat; unknown liveness is ambiguous, not abandoned. Auto-adopt exactly one budget-only partial that is not actively owned after drift and contract validation. If its Session budget expired, preserve it and create a linked successor rather than rewriting history. Ambiguous, safety-blocked, failed, or drift-conflicted runs require explicit recovery or read-only orientation. An explicitly disjoint run may proceed only after recording protected paths and capability boundaries.

## Run ledger

Create `docs/software-evolution/runs/RUN-*.md` (or configured equivalent) from [../templates/autopilot-run.md](../templates/autopilot-run.md). Record:

- Profile, scope, start/deadline, branch/HEAD/worktree identity, parseable invocation owner/session deadline/heartbeat metadata, effective config source, and defaulted paths.
- Session hard limits, current Window limits, Window Ledger, Implementation/Governance accounting, and verification floor/actual time.
- Every `BATCH-*`, finding chosen/skipped, exact verification result, and changed files by class.
- Decisions, specialist handoffs, protected-operation blockers, environment failures, and terminal stop reason.
- Aggregate verification and whether the next plain invocation may auto-adopt, or explicit `resume` is required.

## Continuous selection and failure policy

After each batch, re-read current evidence and select again. Prefer work that reduces user/business harm, data/security/availability risk, recurrent failure, architecture multiplication, and verification gaps.

- One failing check triggers diagnosis, not blind retry.
- Three failures of the same repair hypothesis stop that hypothesis.
- Respect `max_consecutive_failed_batches`; when reached, end the writable path and preserve evidence.
- Before a budget stop, search for a smaller independent batch instead of assuming the largest candidate is the only option.
- When remaining wall-clock time reaches the verification floor, stop new edits and use the remainder only for verification and handoff. Performing verification does not consume the floor into a zero balance.

## Completion language

An unattended run may report `session budget complete`, `safe work exhausted`, `blocked`, or `interrupted`. A normal Window checkpoint is not a final result. Claim repository-wide completion only when the declared repository-wide scope was actually covered and all required evidence passed; otherwise identify the covered slice and remaining queue.
