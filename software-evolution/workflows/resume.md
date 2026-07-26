# Resume Run or Batch

`WRITE POLICY: INHERITED_OR_READ_ONLY`

Use explicit `resume` for a genuinely interrupted, drifted, ambiguous, or specifically targeted `RUN-*` or `BATCH-*`. Normal Autopilot Budget Window rollover must continue in the same invocation, and default Autopilot handles a unique budget-only partial run automatically.

## Procedure

1. Resolve the supplied ID/path. For `RUN-*`, read the ledger created from [../templates/autopilot-run.md](../templates/autopilot-run.md), verify its profile/status/repository identity/session and window budgets, and resolve its `latest_batch_id`. For `BATCH-*`, resolve [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md) directly. If multiple equally relevant runs/batches exist, do not guess.
2. Read the originating mode, target, decision/approval state, Session and Window consumption, verification status, stop reason, and next safe action. If no valid batch checkpoint exists, remain read-only and rebuild orientation before creating a new batch.
3. Validate project configuration with JSON output and use `effective_config`; do not recreate legacy ad hoc budgets. Run:

```bash
python3 <skill-root>/scripts/check_checkpoint_drift.py \
  --root "$PWD" --checkpoint <latest-batch-file>
```

4. Handle drift:
   - `NO_DRIFT`: re-run the last passed gate, then continue under the proven original contract.
   - `SAFE_DRIFT`: inspect new untracked/out-of-scope artifacts and continue only if they cannot affect the batch. Refresh the persisted fingerprint only when the inherited contract permits checkpoint writes.
   - `MATERIAL_DRIFT`: remain read-only, rebuild affected evidence, and do not edit until current policy re-authorizes the batch.
   - `CONFLICTING_DRIFT`: stop the old repair path; report the branch/scope conflict and create a new batch only under a valid writable contract.
   - `UNKNOWN`: remain read-only and reconstruct orientation manually.
5. Revalidate time-sensitive dependencies, generated artifacts, environments, approvals, business decisions, and the last successful verification. Discard invalidated conclusions.
6. Preserve consumed Session budget when continuing the same run. If its deadline or hard limits expired, do not pretend they reset; either finish read-only or create a linked successor run under an independently valid writable invocation.
7. Continue from the smallest safe step while preserving the verification floor. A resumed Autopilot/Overnight run updates its parent ledger after every batch and follows its current continuation contract.

## Safety rules

- `resume` never creates authority that the original batch lacked.
- Expired or ambiguous production/permission approvals must be requested again.
- If the original mode cannot be proven, use the read-only exit and report the evidence needed to continue.
- Do not use `resume` as a workaround for ordinary Window rollover or to reset consumed limits inside one run.
