# P12 Container Package

```bash
docker compose -f products/revenue-reconciliation-ai/deploy/docker-compose.yml up --build
```

The non-root container drops capabilities, uses a read-only filesystem and stores demo runtime state in tmpfs. It is not approved for live bank, provider, tax, revenue or treasury data.
