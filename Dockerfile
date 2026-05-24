FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
    "fastapi>=0.115" "uvicorn[standard]>=0.32" "pydantic>=2.9" "pyyaml>=6.0" \
    "structlog>=24" "opentelemetry-api>=1.28" "opentelemetry-sdk>=1.28" \
    "opentelemetry-exporter-otlp>=1.28" "opentelemetry-instrumentation-fastapi>=0.49" \
    "prometheus-client>=0.21"

COPY src/ ./src/
COPY workflows/ ./workflows/
COPY catalog/ ./catalog/

RUN addgroup --system kdd && adduser --system --ingroup kdd --uid 1000 kdd \
    && chown -R kdd:kdd /app

USER kdd

ENV PYTHONPATH=/app/src
ENV HOST=0.0.0.0
ENV PORT=8070
ENV WORKFLOWS_ROOT=/app

EXPOSE 8070

CMD ["python", "-m", "workflow_registry.main"]
