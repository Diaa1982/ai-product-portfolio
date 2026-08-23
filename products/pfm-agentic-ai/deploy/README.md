# P01 Container Package

From repository root, copy `.env.example` to `.env` if a non-default port is required, then run:

```bash
docker compose -f products/pfm-agentic-ai/deploy/docker-compose.yml up --build
```

The container runs as a non-root user, drops Linux capabilities, uses a read-only filesystem and keeps demo runtime state in tmpfs. These settings are a baseline, not a production security approval.
