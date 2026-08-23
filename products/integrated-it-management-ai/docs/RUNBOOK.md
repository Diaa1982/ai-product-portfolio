# Runbook

Check `/health`, dependencies, event freshness, queue/quarantine, calculation version, evidence resolution, error rate and latency. For degraded inputs, preserve the last approved view, label it stale, stop affected recommendations and notify data/service owners. For security, integrity or authorization incidents, isolate affected connectors, preserve logs/evidence and follow the organizational incident plan.

Rollback uses the prior signed image and configuration after authority approval; reconcile events received during the interruption. Never delete or rewrite decision/audit history. Escalate protected actions, high residual risk, systemic SLA failure, control-evidence gaps and suspected data tampering to named accountable roles.
