# Resume Mode

`WRITE POLICY: INHERITED_OR_READ_ONLY`

Resume an interrupted `BATCH-*` only after proving that its assumptions and write contract remain valid.

## Procedure

1. Resolve the checkpoint created from [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md) using the supplied ID/path or the latest active batch index. If multiple equally relevant batches exist, do not guess.
2. Read the checkpoint, originating mode, target, decision/approval state, budget consumption, verification status, and next safe action.
3. Validate project configuration and run:

```bash
python3 <skill-root>/scripts/check_checkpoint_drift.py \
  --root "$PWD" --checkpoint <batch-file>
```

4. Handle drift:
   - `NO_DRIFT`: re-run the last passed gate, then continue under the original mode.
   - `SAFE_DRIFT`: inspect new untracked/out-of-scope artifacts and continue only if they cannot affect the batch. Refresh the persisted fingerprint only when the inherited contract permits checkpoint writes.
   - `MATERIAL_DRIFT`: remain read-only, rebuild affected evidence, and do not edit until current policy re-authorizes the batch. Persist a revised checkpoint only when the inherited control-plane write contract permits it.
   - `CONFLICTING_DRIFT`: stop the old repair path; report the branch/scope conflict and create a new batch only under a valid writable contract.
   - `UNKNOWN`: remain read-only and reconstruct orientation manually.
5. Revalidate time-sensitive dependencies, generated artifacts, environments, approvals, business decisions, and the last successful verification.
6. Discard conclusions invalidated by new code/runtime evidence.
7. Continue from the smallest safe step while preserving remaining verification reserve.

## Safety rules

- `resume` never creates authority that the original batch lacked.
- Expired or ambiguous production/permission approvals must be requested again.
- If the original mode cannot be proven, use the read-only exit and report the evidence needed to resume.
