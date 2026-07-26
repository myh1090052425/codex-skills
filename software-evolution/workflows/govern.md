# Govern Mode

Continuously govern the most relevant recent or high-value scope, repair safe findings, and leave the system more coherent than before.

## Scope selection

1. Prefer user-specified scope.
2. Otherwise inspect uncommitted changes and the current branch diff against its likely base.
3. If there is no meaningful diff, select the highest-priority `ready` debt item or a critical flow with weak coverage.
4. Keep the batch small enough to edit, test, re-scan, and document in the current run.

## Procedure

1. Read the common loop and current project memory.
2. Determine which capabilities, user journeys, modules, contracts, and tests the selected changes affect.
3. Run the capability reuse gate before accepting new services, endpoints, components, DTOs, validators, permission rules, queries, or utilities.
4. Inspect the scope across the three pillars:
   - User/business outcome and interaction quality.
   - Engineering correctness, reliability, and maintainability.
   - Architecture boundaries, reuse, and evolution impact.
5. Prove and rank findings. Ignore style preferences that have no operational, user, business, or evolution cost.
6. Autonomously repair the highest-value low-risk coherent batch when verification is available.
7. Add regression tests and run targeted plus risk-appropriate broader checks.
8. For UI changes, execute the affected browser flow when locally runnable.
9. Re-scan the diff for duplicate capability, rule fragmentation, new coupling, dead branches, and missing feedback/error handling.
10. Update memory and debt; close only findings with verification evidence.
11. Continue with another batch only if it remains safe and fully verifiable.

## Default output

Return a compact governance summary. Include a detailed finding record only for unresolved or high-risk issues, or when the user requests a full report.
