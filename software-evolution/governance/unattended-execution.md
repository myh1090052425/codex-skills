# Unattended Execution Governance

Enable sustained autonomous work without converting absence into unlimited authority.

## Profiles

- `autopilot`: default no-argument run; automatically initializes when needed and performs multiple safe governance batches within the normal budget.
- `overnight`: longer unattended run using `overnight_budget`, stronger isolation, a deadline, a final verification reserve, and a durable `RUN-*` ledger.

Neither profile requires the user to run `init`, `audit`, or `govern` first.

## Authorization envelope

The invocation authorizes only repository-local, reversible, evidence-backed R1 and bounded R2 source/test/control-plane edits allowed by configuration and repository rules. It does not authorize production or shared-data mutation, deployment, remote publication, destructive Git operations, credentials, permissions, billing, or R3/R4 semantic changes.

## Isolation and user work

1. Prefer a Codex isolated worktree for overnight runs.
2. If running in the current checkout, inspect branch, HEAD, worktree and untracked files before editing.
3. Preserve all pre-existing user changes. Do not stash, reset, clean, overwrite, or absorb them into a repair.
4. If changed paths overlap a candidate batch, skip/checkpoint that batch or work in a separately provided isolated worktree.

## Run ledger

Create `docs/software-evolution/runs/RUN-*.md` (or configured equivalent) from [../templates/autopilot-run.md](../templates/autopilot-run.md). Record:

- Profile, scope, start/deadline, branch/HEAD/worktree identity.
- Time/cycle/batch/file/finding budgets and verification reserve.
- Every `BATCH-*`, finding chosen/skipped, exact verification result, and changed files.
- Decisions, specialist handoffs, protected-operation blockers, environment failures, and stop reason.
- Aggregate verification and the next safe resume action.

## Continuous selection

After each batch, re-read the current system evidence and select again. Do not treat the initial finding list as permanently authoritative. Prefer work that reduces user/business harm, data/security/availability risk, recurrent failure, architecture multiplication, and verification gaps.

## Failure policy

- One failing check triggers diagnosis, not blind retry.
- Three failures of the same repair hypothesis stop that hypothesis.
- Respect `max_consecutive_failed_batches`; when reached, enter final verification/checkpoint and stop.
- Infrastructure/rate-limit/tool failures are recorded separately from product failures.
- Never weaken or delete a test merely to make the run green unless authoritative behavior proves the test obsolete.

## Time and verification reserve

Track elapsed time conservatively. Do not begin a batch unless enough time remains to repair, run narrow checks, run required broader checks, inspect the diff, update memory, and checkpoint. When the reserve boundary is reached, stop discovery and editing immediately and use the remainder only for verification and handoff.

## Completion language

An unattended run may report `budget complete`, `safe work exhausted`, `blocked`, or `interrupted`. It may claim the repository is clean only if the declared repository-wide scope was actually covered and all required evidence passed. Otherwise identify the covered slice and remaining queue.
