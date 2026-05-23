"""Health and metrics for workflow-registry-service."""
import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        service="workflow-registry-service",
        version="0.1.0",
        environment=os.getenv("APP_ENV", "local"),
    )


@router.get("/metrics")
async def metrics():
    return {"service": "workflow-registry-service", "metrics": {}}
