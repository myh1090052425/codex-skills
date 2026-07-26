# Resume Run or Batch

`WRITE POLICY: INHERITED_OR_READ_ONLY`

Use explicit `resume` for a drifted, ambiguous, specifically targeted, or otherwise non-auto-adoptable `RUN-*` or `BATCH-*`. Normal batch checkpoints continue automatically. Default Autopilot handles one unique drift-safe host-interrupted or legacy-quota partial without requiring `resume`.

## Procedure

1. Resolve the supplied ID/path. For `RUN-*`, read [../templates/autopilot-run.md](../templates/autopilot-run.md), verify profile/status/repository identity/owner, and resolve `latest_batch_id`. For `BATCH-*`, resolve [../templates/batch-checkpoint.md](../templates/batch-checkpoint.md). If multiple equally relevant candidates exist, do not guess. If no valid checkpoint metadata exists, remain read-only and rebuild orientation before creating any new batch.
2. Read the originating mode, target, authority, verification status, real stop reason, changed-path telemetry, and next safe action. Treat historical file/cycle/window/finding/batch quotas as deprecated evidence, never as remaining authority or stop conditions.
3. Validate project configuration with JSON output and use `effective_config`. Record and ignore `deprecated_paths`. Run:

```bash
python3 <skill-root>/scripts/check_checkpoint_drift.py \
  --root "$PWD" --checkpoint <latest-batch-file>
```

4. Handle drift:
   - `NO_DRIFT`: re-run the last passed gate, then continue under the proven original contract.
   - `SAFE_DRIFT`: inspect new untracked/out-of-scope artifacts and continue only if they cannot affect the batch.
   - `MATERIAL_DRIFT`: rebuild affected evidence before writing.
   - `CONFLICTING_DRIFT`: stop the old path; create a new batch only under a valid non-conflicting contract.
   - `UNKNOWN`: remain read-only and reconstruct orientation.
5. Revalidate time-sensitive dependencies, generated artifacts, environments, approvals, business decisions, and the last successful verification. Discard invalidated conclusions.
6. Continue from the smallest safe semantic step. Do not reset or recreate obsolete quota counters. A resumed Autopilot/Overnight/Deep run checkpoints each batch and continues until a real stop condition.

## Safety rules

- `resume` never creates authority the original batch lacked.
- Expired or ambiguous production/permission approvals must be requested again.
- If the original write contract cannot be proven, use the read-only exit.
- Do not use `resume` to restart work after a normal checkpoint; continuation should already be automatic.
