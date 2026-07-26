# Evolution and Business Consistency Governance

Make every feature change pass a convergence gate so repeated AI-assisted development does not accumulate permanent patches.

## Post-change evolution gate

After implementing any requirement, answer:

1. What user journey and business capability changed?
2. Which existing capability was reused or extended?
3. Did the change introduce a parallel service, endpoint, component, DTO, validator, permission rule, query, or utility?
4. Did responsibility move across a module or domain boundary?
5. Did an `if/else`, feature flag, compatibility branch, fallback, or temporary adapter become permanent?
6. Did the change create a new source of truth, state transition, field meaning, or data representation?
7. Should an existing abstraction be simplified instead of adding another layer?
8. Which tests prove old and new behavior together?
9. Which memory and debt entries must change?

Do not close the requirement until the answers are evidenced or explicitly recorded as debt.

## Detect software rot

Look for trends, not isolated aesthetics:

- Multiple patches around the same invariant or state transition.
- Increasing branch count in a central workflow.
- Temporary feature flags or adapters without removal criteria.
- Multiple modules writing the same aggregate or table.
- Repeated domain translation at many callers.
- Tests that mock the real rule owner differently in each module.
- New code that bypasses an existing use case or canonical capability.
- Shared layers that grow flags and caller-specific exceptions.
- Documentation/memory that no longer matches runtime behavior.

Prefer removing the underlying decision ambiguity, ownership gap, or missing seam over adding another patch.

## Business consistency inventory

Compare across modules:

- State machines and allowed transitions.
- Enum/status definitions and display mappings.
- Field names, units, nullability, defaults, and lifecycle meaning.
- Validation thresholds, formulas, date/time boundaries, and rounding.
- Authorization conditions, tenancy scope, ownership, and role semantics.
- Core calculations, eligibility rules, pricing/risk/scoring logic, and error semantics.
- Query filters that encode business inclusion/exclusion rules.

## Prove a rule split

For each suspected inconsistency:

1. Identify the same business question being answered in multiple places.
2. Extract each rule's inputs, thresholds, state assumptions, and outputs.
3. Find the authoritative source: domain docs, accepted tests, canonical service, schema constraint, product behavior, or owner decision.
4. Trace affected callers and historical data implications.
5. Classify:
   - Intentional context-specific rule.
   - Versioned/deprecated rule.
   - Accidental divergence.
   - Unknown authority.

Unify only accidental divergence with an authoritative target. Record unknown authority as blocked debt rather than choosing whichever implementation looks cleaner.

## Convergence strategy

- Put the canonical invariant near its domain owner.
- Expose one stable capability or policy interface.
- Keep UI/API-specific formatting outside the rule.
- Replace callers incrementally and preserve compatibility where required.
- Add table-driven/contract tests covering thresholds, boundaries, state transitions, and permissions.
- Remove obsolete branches after usage and tests prove migration completion.
- Record the decision and historical reason in architecture memory.

## Patch budget

Treat a new compatibility branch as debt unless it has:

- A documented reason.
- An owner or removal trigger.
- A measurable exit condition.
- Test coverage for both paths.
- A target date/version when meaningful.
