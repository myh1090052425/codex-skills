# Decision Governance

Turn ambiguity into a bounded, answerable decision instead of guessing or stopping with a vague request.

## Create a `DEC-*` record when

- Multiple implementations answer the same business question differently and no authority is clear.
- A change alters business semantics, permission behavior, data ownership, lifecycle/state transitions, public contracts, retention, or compatibility commitments.
- Two safe technical options have materially different user, operational, cost, or evolution consequences.
- A repair or release depends on a product/operations/security decision rather than more code inspection.

## Decision package

Use [../templates/decision-record.md](../templates/decision-record.md) and include:

1. The smallest decision question that unlocks progress.
2. Authoritative information already found and the exact missing authority.
3. Affected actors, capabilities, data, callers, contracts, releases, and debt/findings.
4. Two or three viable options, including compatibility, migration, risk, operational cost, and reversibility.
5. Recommended option with evidence and explicit assumptions.
6. Consequence of delaying or making no decision.
7. The exact operation/phase that requires approval.
8. Final decision, approver/source, date, scope, and supersession trigger when known.

## State model

Use `proposed`, `approved`, `rejected`, `superseded`, or `expired`.

- Only an authoritative user/source can move a business decision to `approved`.
- A technical choice fully inside an already-authorized R1/R2 batch may be decided by the Agent when semantics and contracts do not change; record the rationale when material.
- Expire time-sensitive rollout, emergency, or production decisions when their stated window ends.

## Execution gate

- Continue independent discovery and reversible preparation while a decision is pending.
- Do not implement the branch whose semantics depend on an unapproved decision.
- After approval, re-check current code, branch, migrations, consumers, risk, and verification coverage before execution; old evidence may have drifted.
- Link the decision ID from findings, repair plans, checkpoints, capability map, and architecture memory.
