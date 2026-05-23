"""Workflow Registry Service — register, validate and expose declarative KDD workflows."""
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware import RequestContextMiddleware
from .routers import health, version, workflows

logger = logging.getLogger(__name__)

SERVICE_NAME = "workflow-registry-service"
VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Starting %s v%s", SERVICE_NAME, VERSION)
    yield
    logger.info("Shutting down %s", SERVICE_NAME)


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

app.include_router(health.router, tags=["health"])
app.include_router(version.router, tags=["version"])
app.include_router(workflows.router, prefix="/workflows", tags=["workflows"])

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
