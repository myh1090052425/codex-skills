# Observe Mode

`WRITE POLICY: READ_ONLY`

Connect real runtime signals to user outcomes, architecture memory, and technical debt. Production access is read-only.

## Procedure

1. Identify the flow/service, actor, business outcome, environment, release/version, and observation window.
2. Map journey steps to SLI/SLO, logs, metrics, traces, alerts, queue/cache/database signals, and user/support evidence.
3. Verify telemetry semantics: what is counted as success, failure, latency, freshness, saturation, loss, retry, and duplicate effect.
4. Look for silent failure, false-success logging, missing correlation, cardinality/retention gaps, alert blind spots, noisy alerts, and unobservable rollback criteria.
5. Correlate incidents, error rates, slow queries, traces, and feedback with code paths and capabilities without assuming causation.
6. Compare measured state with `health-baseline.json` and architecture memory, but never update them in observe mode. With `--record`, persist only the observation report.
7. For proposed repairs, define a post-fix observation window, baseline, target threshold, guardrail, and rollback/stop condition.
8. Return [../templates/observation-report.md](../templates/observation-report.md).

## Prohibited behavior

Do not change alerts, dashboards, sampling, feature flags, production config, data, queues, caches, deployments, or access. Hand off source repairs to `repair`; request explicit approval for any operational write.

## Verdict

Use `HEALTHY_WITHIN_WINDOW`, `DEGRADATION_CONFIRMED`, `OBSERVABILITY_GAP`, `INCIDENT_REVIEW_REQUIRED`, or `INSUFFICIENT_EVIDENCE`.
