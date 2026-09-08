# Deployment

## Management-demo candidate

```bash
cp products/pfm-agentic-ai/deploy/.env.example products/pfm-agentic-ai/deploy/.env
docker compose -f products/pfm-agentic-ai/deploy/docker-compose.yml up --build -d
curl http://localhost:8080/health
```

Open:

- `http://localhost:8080/` — management demonstration.
- `http://localhost:8080/command-center` — configurable agent command center.
- `http://localhost:8080/docs` — OpenAPI.

The container runs non-root, read-only, drops Linux capabilities and uses tmpfs for runtime data. It requires outbound HTTPS access if the live public-signal adapters are to operate. If outbound access or a source is unavailable, the Signals UI displays a degraded state and does not relabel synthetic content as live.

Stop with:

```bash
docker compose -f products/pfm-agentic-ai/deploy/docker-compose.yml down
```

## Optional approved signal sources

Set `PFM_SIGNAL_SOURCES_JSON` to a JSON array of approved public pages. This extends the baseline public adapters; it does not authorize access to internal government data.

## Production gate

Choose an approved hosting environment; pin base images and dependencies; add TLS, SSO/RBAC, secrets management, persistent evidence/audit storage, backups, monitoring, alert routing, WAF/network policy, vulnerability scanning and rollback. Replace generic public-page extraction with validated source-specific APIs/RSS contracts. Configure internal source systems only after data-owner, security, legal, accounting and interface approval. Complete reconciliation, UAT, failure/rollback testing and a limited pilot before go-live.
