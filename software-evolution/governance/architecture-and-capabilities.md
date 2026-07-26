# Architecture and Capability Governance

Protect boundaries and converge business effects without creating abstraction for its own sake.

## Architecture health checks

Inspect:

- Module and deployment boundaries.
- Responsibility and change ownership.
- Dependency direction and forbidden inward/outward references.
- Cycles, shared mutable state, and hidden runtime coupling.
- Domain aggregates, invariants, transactions, and data ownership.
- Public/internal contracts and adapter boundaries.
- High fan-in/out modules and change hotspots.
- Abstractions whose names and APIs express domain intent.
- Pass-through layers, wrapper chains, “common” dumping grounds, and speculative frameworks.

A boundary issue is material when it causes rule duplication, unsafe change propagation, inconsistent transactions, testing difficulty, release coupling, or unclear ownership.

## Define a business capability signature

Represent each capability with:

```text
Capability = actor intent
           + business outcome/state effect
           + primary aggregate/data ownership
           + inputs and outputs
           + invariants and authorization
           + side effects/events
           + entry points and callers
```

Names and code similarity are supporting signals, not the definition.

## Discover duplicate capabilities

1. Inventory candidates from:
   - Routes/endpoints, UI actions, commands, jobs, consumers, service methods, domain methods, and repository operations.
   - Domain verbs and synonyms such as update/modify/change/adjust.
   - Shared aggregates, tables, events, status transitions, validators, permissions, and result DTOs.
2. Normalize each candidate into a capability signature.
3. Cluster candidates by the same business outcome or state effect.
4. Trace callers and side effects to determine whether they are:
   - `canonical`: owns the invariant and business effect.
   - `adapter`: translates protocol/context into the canonical capability.
   - `specialization`: intentionally adds narrower rules while reusing the base invariant.
   - `duplicate`: independently owns substantially the same effect and rules.
   - `uncertain`: evidence or business authority is insufficient.
5. Record evidence and classification in `capability-map.md`.

## Decide whether to converge

Converge when:

- The business outcome and invariant are the same.
- Independent implementations can drift or already conflict.
- One implementation can own the transaction/data effect.
- Callers can migrate without an unsafe contract break.

Do not converge when:

- Similar verbs operate on different aggregates or lifecycle stages.
- Protocol, latency, consistency, tenancy, or permission boundaries legitimately differ.
- A shared abstraction would expose a union of unrelated options or require caller-specific branching.
- The duplication is cheaper and safer than the coupling it would introduce.

## Convergence pattern

Prefer:

1. Select or create one domain-named canonical capability.
2. Move invariants and state transitions into that owner.
3. Keep thin adapters at UI/API/job/event boundaries.
4. Migrate callers incrementally with characterization tests.
5. Remove duplicate behavior only after all callers and side effects are verified.
6. Update the capability map and architecture memory.

Avoid:

- Wrapper around wrapper.
- Manager/facade/service pass-through chains.
- Generic utility APIs with flags for unrelated business variants.
- Shared DTOs that leak one module's model into all others.
- Centralization that violates data or deployment ownership.

## New capability gate

Before implementing a new capability, require documented answers:

- Which capability-map terms and synonyms were searched?
- Which existing implementations were compared?
- Why reuse, extension, adapter, or a new canonical capability is correct?
- What invariant owner and data boundary will own the effect?
- How will the capability be tested and recorded?

If these answers are missing, do not add the new implementation yet.
