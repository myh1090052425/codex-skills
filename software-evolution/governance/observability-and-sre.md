# Observability and SRE Governance

Use runtime evidence to test whether the system delivers business outcomes reliably. Telemetry volume alone is not observability.

## Map outcome to signal

For each critical journey or service, record:

- Actor and intended business result.
- Entry point and important internal stages.
- SLI definition, unit, population, exclusions, and data source.
- SLO/threshold and error-budget meaning when authoritative.
- Logs, metrics, traces, events, query/queue/cache signals, and alert coverage.
- Version/release and observation window.

Prefer outcome SLIs (orders successfully finalized) over proxy-only SLIs (HTTP 200 rate) when possible.

## Detect failure modes

Check for:

- Exceptions swallowed or converted to false success.
- Success metrics emitted before durable business completion.
- Retries counted as independent successes or failures without deduplication.
- Missing correlation IDs or broken trace propagation.
- No visibility into queues, scheduled jobs, cache staleness, replication lag, or partial writes.
- Alerts with no user impact mapping, noisy thresholds, missing burn-rate/volume context, or no owner/runbook.
- Sampling, cardinality, retention, clock, or aggregation choices that hide critical behavior.
- Architecture memory or health baseline that contradicts current runtime evidence.

## Convert runtime evidence into governance

A runtime-derived finding must include window, environment, query/filter, sample size or event count when available, version, baseline, affected capability, code path, and alternative explanations. Correlation is not root-cause proof.

For a repair, define:

- Pre-fix baseline.
- Expected signal movement and guardrails.
- Observation window long enough for the relevant traffic/cron cycle.
- Success, rollback, and inconclusive thresholds.
- Who/what will verify after rollout.

Use [../templates/incident-review.md](../templates/incident-review.md) for material incidents and [../templates/observation-report.md](../templates/observation-report.md) for observation batches.

## Safety boundary

Default to production read-only. Do not change telemetry, sampling, dashboards, alerts, flags, deployments, queues, data, or permissions without explicit approval. Redact secrets and sensitive/user-identifying data from durable reports.
