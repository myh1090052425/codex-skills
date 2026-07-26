# Resume Run or Batch

`WRITE POLICY: INHERITED_OR_READ_ONLY`

Resume an interrupted `RUN-*` or `BATCH-*` only after proving that its assumptions, budget, repository identity, and write contract remain valid.

## Procedure

1. Resolve the supplied ID/path. For `RUN-*`, read the ledger created from [../templates/autopilot-run.md](../templates/autopilot-run.md), verify its profile/status/repository identity/budget, and resolve its `latest_batch_id`. For `BATCH-*`, resolve [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md) directly. If multiple equally relevant runs/batches exist, do not guess.
2. Read the run ledger and/or checkpoint, originating mode, target, decision/approval state, budget consumption, verification status, stop reason, and next safe action. If a run has no valid batch checkpoint yet, remain read-only and rebuild orientation before creating a new batch.
3. Validate project configuration and run:

```bash
python3 <skill-root>/scripts/check_checkpoint_drift.py \
  --root "$PWD" --checkpoint <latest-batch-file>
```

4. Handle drift:
   - `NO_DRIFT`: re-run the last passed gate, then continue under the original mode.
   - `SAFE_DRIFT`: inspect new untracked/out-of-scope artifacts and continue only if they cannot affect the batch. Refresh the persisted fingerprint only when the inherited contract permits checkpoint writes.
   - `MATERIAL_DRIFT`: remain read-only, rebuild affected evidence, and do not edit until current policy re-authorizes the batch. Persist a revised checkpoint only when the inherited control-plane write contract permits it.
   - `CONFLICTING_DRIFT`: stop the old repair path; report the branch/scope conflict and create a new batch only under a valid writable contract.
   - `UNKNOWN`: remain read-only and reconstruct orientation manually.
5. Revalidate time-sensitive dependencies, generated artifacts, environments, approvals, business decisions, and the last successful verification.
6. Discard conclusions invalidated by new code/runtime evidence.
7. Continue from the smallest safe step while preserving remaining verification reserve. For a resumed Autopilot/Overnight run, update the parent `RUN-*` ledger after every batch and continue until its remaining stop/budget conditions are reached.

## Safety rules

- `resume` never creates authority that the original batch lacked.
- Expired or ambiguous production/permission approvals must be requested again.
- If the original mode cannot be proven, use the read-only exit and report the evidence needed to resume.
