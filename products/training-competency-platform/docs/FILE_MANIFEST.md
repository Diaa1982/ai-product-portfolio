# MVP file manifest

The original deployable ZIP contains these files. The source package is the runnable release; the earlier GitHub `index.html` is an unrelated, smaller browser-only demonstration.

| Path | Description |
|---|---|
| `README.md` | Package overview and quick start |
| `docs/IMPLEMENTATION.md` | Workflow, implemented schema, gaps and acceptance criteria |
| `Dockerfile` | Python 3.12 image, dependencies, backend/frontend copy and startup |
| `docker-compose.yml` | PostgreSQL 16, app service, DB health check, volume and port binding |
| `.env.example` | Database password and loopback binding template |
| `.dockerignore` | Excludes secrets, Git and caches from image build |
| `.gitignore` | Excludes local secrets, SQLite database and caches from version control |
| `requirements.txt` | Pinned Python dependencies |
| `app/main.py` | FastAPI routes, SQLAlchemy tables, deterministic grading, progression and audit |
| `app/seed.py` | Six demo users, approved synthetic document, programme, two modules and four questions |
| `web/index.html` | **Connected frontend**, served by FastAPI at `http://localhost:8000` |
| `tests/test_workflow.py` | Pytest fail/pass/critical gate and progression test |
| `index.html` | Earlier independent localStorage/browser-only prototype; not served by FastAPI |

**Editing map:** change `web/index.html` for the current connected UI, `app/main.py` for backend and database, `app/seed.py` for demo records, and `docker-compose.yml` for services. Do not commit `.env`. The current GitHub branch initially contained only a short README and browser prototype; the ZIP contains the runnable backend. No public deployment is configured.