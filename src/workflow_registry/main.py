"""Workflow Registry Service — register, validate and expose declarative KDD workflows."""
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from fastapi import Depends

from .middleware import RequestContextMiddleware
from .routers import health, version, workflows
from .security import require_api_key

logger = logging.getLogger(__name__)

SERVICE_NAME = "workflow-registry-service"
VERSION = "0.1.0"


def _configure_otel(app: FastAPI, service_name: str = SERVICE_NAME) -> None:
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")
    if not endpoint:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True)))
        trace.set_tracer_provider(provider)
        FastAPIInstrumentor.instrument_app(app)
        logger.info("OTEL tracing enabled → %s", endpoint)
    except Exception as exc:
        logger.warning("OTEL setup failed (non-fatal): %s", exc)


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Starting %s v%s", SERVICE_NAME, VERSION)
    yield
    logger.info("Shutting down %s", SERVICE_NAME)


_REQUEST_COUNT = Counter(
    "workflow_registry_http_requests_total", "Total HTTP requests", ["method", "path", "status_code"]
)

app = FastAPI(
    title="Workflow Registry Service",
    version=VERSION,
    description=(
        "Manages declarative YAML workflow definitions for the KDD agentic platform. "
        "Validates schemas, versions workflows and exposes them to the agent orchestrator."
    ),
    lifespan=lifespan,
)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def _metrics_middleware(request: Request, call_next):
    response = await call_next(request)
    _REQUEST_COUNT.labels(
        method=request.method, path=request.url.path, status_code=response.status_code
    ).inc()
    return response


@app.get("/metrics", include_in_schema=False)
async def _metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


_auth = [Depends(require_api_key)]

app.include_router(health.router, tags=["health"])
app.include_router(version.router, tags=["version"])
app.include_router(workflows.router, prefix="/workflows", tags=["workflows"], dependencies=_auth)

_configure_otel(app)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


def create_app() -> FastAPI:
    return app


def main() -> None:
    import uvicorn
    uvicorn.run(
        "workflow_registry.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8070")),
        log_level="info",
    )


if __name__ == "__main__":
    main()
