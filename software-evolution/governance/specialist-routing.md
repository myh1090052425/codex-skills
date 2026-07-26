# Specialist Routing

The main Skill owns system context, prioritization, cross-domain tradeoffs, and integration. Route deep specialist work instead of expanding the core workflow indefinitely.

## Routing protocol

1. Detect a trigger from evidence, not keywords alone.
2. Define the exact question, scope, target identity, trust/environment boundary, and evidence already collected.
3. Load an available specialist Skill/tool and obey its prerequisites before using it.
4. Preserve the current mode contract. A read-only parent mode cannot gain write authority through a specialist.
5. Request a bounded output: confirmed findings, proof gaps, affected paths/callers, risk, and next verification.
6. Reconcile specialist output with business capabilities, architecture, release, and testing gates.
7. Treat config value `off` as disabling automatic dispatch, not as lowering the evidence/safety gate. If no suitable specialist exists, create [../templates/specialist-handoff.md](../templates/specialist-handoff.md) and keep uncertain conclusions labeled.

## Trigger matrix

| Domain | Route when evidence involves | Expected specialist output |
|---|---|---|
| Security/privacy | Authentication, authorization, trust boundaries, secrets, injection, tenant isolation, sensitive data, threat paths | Threat model/findings, exploitability, affected boundary, verified fix or hardening plan |
| Supply chain | Vulnerable/EOL dependencies, licenses, lockfile drift, unsigned/unpinned build sources, compromised artifact provenance | Dependency reachability, upgrade/compatibility plan, provenance/licensing evidence |
| Data governance | Quality, lineage, freshness, reconciliation, retention/deletion, backfill, schema ownership, PII handling | Data contracts, validation/query evidence, migration/reconciliation plan |
| Performance/cost | Latency, throughput, capacity, query plans, hot paths, cloud/API spend, performance budgets | Baseline, bottleneck/cost driver, experiment, target and guardrail |
| UX/accessibility | Navigation, journey friction, interaction state, browser behavior, WCAG-relevant behavior | Runtime evidence, affected actors/flows, screenshots/traces, post-fix flow |
| Database | Indexes, transactions, locks, deadlocks, migrations, replication, backup/recovery | Query/lock evidence, migration/rollback/recovery validation |
| CI/CD/release | Failing checks, artifact mismatch, deployment ordering, environment drift | Exact failing gate, logs/artifact identity, remediation and release impact |

## Guardrails

- Do not expose private repository code, logs, secrets, or production data to an external tool unless the current environment and user authorization permit it.
- Do not route merely to obtain a second opinion on a trivial local issue.
- Do not accept specialist output without checking repository-local evidence and scope.
- Do not duplicate specialist findings as multiple debt items; keep one canonical ID and link evidence.
