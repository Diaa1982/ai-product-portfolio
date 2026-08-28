FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
EXPOSE 8000 7860
CMD ["uvicorn", "enterprise_ai.api:app", "--host", "0.0.0.0", "--port", "8000"]

