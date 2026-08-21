FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PRODUCT_REGISTRY_PATH=/app/products/registry.json

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY products ./products

EXPOSE 8000

CMD ["uvicorn", "src.portfolio_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
