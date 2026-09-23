# Local Docker deployment runbook

## Requirements
A Windows/macOS/Linux computer with Docker Engine and Docker Compose. The iPhone HTML file preview cannot run the backend.

## Setup
Extract the deployable ZIP and open a terminal in the directory containing `Dockerfile`, `docker-compose.yml` and `.env.example`.

```sh
docker --version
docker compose version
cp .env.example .env
```

Windows PowerShell alternative: `Copy-Item .env.example .env`. Edit `.env` to set:

```dotenv
POSTGRES_PASSWORD=REPLACE_WITH_LONG_LOCAL_PASSWORD
APP_BIND=127.0.0.1
```

The password initializes the PostgreSQL user on first creation of the data volume. Changing it later in `.env` does not rotate the database user's existing password. Loopback binding prevents other devices from reaching the insecure demo application.

```sh
docker compose config
docker compose up --build -d
docker compose ps
docker compose logs --tail=100 app
```

Open `http://localhost:8000` (connected frontend), `http://localhost:8000/docs` (API explorer), `http://localhost:8000/api/health` (health). Compose provisions PostgreSQL 16 Alpine with database/user `training`, a health check, named volume `pgdata`, and app container listening on port 8000. On startup the app runs `python -m app.seed`, then Uvicorn.

## Test and stop
Choose Demo Learner; open the seeded published programme and attempt module 1. A critical-control failure prevents module 2; a successful reassessment unlocks it. `docker compose logs -f app` streams logs. `docker compose down` stops services and preserves the DB. `docker compose down -v` **deletes the database volume**.

## Without Docker
Create a Python virtual environment, install `requirements.txt`, run `python -m app.seed`, then `uvicorn app.main:app --reload`. Without `DATABASE_URL`, the app uses local SQLite `training.db`. Run `pytest -q` separately.

## Troubleshooting
If Docker cannot connect, start Docker Desktop. If the app cannot reach PostgreSQL, check `docker compose ps` and DB logs and verify the password used at initial volume creation. If port 8000 is occupied, stop the conflicting process or change host port mapping. Do not open the standalone HTML in iPhone preview; it is not the connected application. Do not widen `APP_BIND` for remote testing until proper authentication and security controls exist.