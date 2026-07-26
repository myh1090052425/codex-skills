# Audit Mode

`WRITE POLICY: READ_ONLY`

Prove, classify, and prioritize issues without changing the system.

## Target

Accept a file/module/flow/capability/debt ID/diff/branch or repository scope. If omitted, inspect current changes first, then critical flows and high-risk hotspots.

## Procedure

1. Execute the shared evidence phases in the common loop.
2. Declare target identity, coverage worklist, evidence sources, exclusions, and completion criteria.
3. Inspect user/business outcomes, engineering/reliability, architecture/evolution, testing, and applicable specialist triggers.
4. Reproduce or triangulate findings where safe. Do not run commands that may mutate tracked files, shared data, or external systems.
5. Separate confirmed, probable, and candidate findings. Trace material findings to root cause and call chain.
6. Rank by impact, confidence, recurrence, architecture multiplication, and repair/verifiability.
7. Create decision-ready questions for ambiguous business or contract choices.
8. Return an audit report using [../templates/audit-report.md](../templates/audit-report.md).

## Prohibited behavior

- Do not repair, refactor, format, update tests, change memory/config, or stage files.
- Do not label a candidate as repair-ready.
- Do not persist output unless `--record` or an explicit persistence request is present.
- When recording, write only the audit report under `reports/audit/` and any explicit `DEC-*` package under `decisions/` (or configured equivalents); re-read each destination first.

## Verdict

Use one:

- `CLEAR_WITHIN_SCOPE`
- `FINDINGS_CONFIRMED`
- `DECISION_REQUIRED`
- `SPECIALIST_REQUIRED`
- `INSUFFICIENT_EVIDENCE`

For repair-ready items, supply stable `FIND-*`/`DEBT-*` IDs and the next command: `$software-evolution repair <id>`.
