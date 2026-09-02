FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    RESTAURANT_AI_DATA=/app/data/restaurants.json \
    RESTAURANT_AI_AUDIT=/app/audit/events.jsonl

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir '.[ui,mcp,openai]'
COPY data ./data
RUN mkdir -p /app/audit && useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 7860
CMD ["python", "-m", "restaurant_ai.app"]

