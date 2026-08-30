.PHONY: install test api ui mcp

install:
	python -m pip install -e ".[dev]"

test:
	python -m compileall -q src
	pytest -q

api:
	uvicorn enterprise_ai.api:app --reload

ui:
	python -m enterprise_ai.ui

mcp:
	python -m enterprise_ai.mcp_server

