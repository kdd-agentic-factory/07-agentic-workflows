"""Version endpoint."""
import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class VersionResponse(BaseModel):
    service: str
    version: str
    commit: str
    build_time: str


@router.get("/version", response_model=VersionResponse)
async def version():
    return VersionResponse(
        service="workflow-registry-service",
        version="0.1.0",
        commit=os.getenv("GIT_COMMIT", "unknown"),
        build_time=os.getenv("BUILD_TIME", "unknown"),
    )
