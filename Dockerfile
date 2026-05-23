FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

COPY src/ ./src/

ENV PYTHONPATH=/app/src
ENV HOST=0.0.0.0
ENV PORT=8070

EXPOSE 8070

CMD ["python", "-m", "workflow_registry.main"]
