"""Workflow registry endpoints — list, validate and render KDD workflows."""
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from workflow_registry.services.workflow_service import WorkflowService

router = APIRouter()

_service = WorkflowService(root=os.getenv("WORKFLOWS_ROOT", "."))


class WorkflowSummary(BaseModel):
    workflow_id: str
    name: str
    description: str
    version: str
    triggers: List[str]


class WorkflowValidationResult(BaseModel):
    workflow_id: str
    valid: bool
    errors: List[str]
    warnings: List[str]


class WorkflowRenderResult(BaseModel):
    workflow_id: str
    rendered: Dict[str, Any]
    context_applied: Dict[str, Any]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("", response_model=List[WorkflowSummary])
async def list_workflows():
    return [
        WorkflowSummary(
            workflow_id=w["workflow_id"],
            name=w["name"],
            description=w["description"],
            version=w["version"],
            triggers=w["triggers"],
        )
        for w in _service.list()
    ]


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    wf = _service.get(workflow_id)
    if wf is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    return wf


@router.get("/{workflow_id}/schema")
async def get_workflow_schema(workflow_id: str):
    wf = _service.get(workflow_id)
    if wf is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    return {
        "workflow_id": workflow_id,
        "steps": wf["steps"],
        "approval_gates": wf["approval_gates"],
        "artifacts": wf["artifacts"],
        "kdd_stages": wf["kdd_stages"],
    }


@router.post("/validate", response_model=WorkflowValidationResult)
async def validate_workflow(workflow: Dict[str, Any]):
    workflow_id = workflow.get("workflow_id", "unknown")
    errors = []
    warnings = []
    if "steps" not in workflow:
        errors.append("Missing 'steps' field")
    if "kdd_stages" not in workflow:
        warnings.append("Missing 'kdd_stages' — traceability may be incomplete")
    if "approval_gates" not in workflow:
        warnings.append("Missing 'approval_gates' — consider adding approval checkpoints")
    return WorkflowValidationResult(
        workflow_id=workflow_id,
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


@router.post("/render", response_model=WorkflowRenderResult)
async def render_workflow(workflow_id: str, context: Dict[str, Any] = {}):
    wf = _service.get(workflow_id)
    if wf is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    rendered = dict(wf)
    rendered["context"] = context
    return WorkflowRenderResult(
        workflow_id=workflow_id,
        rendered=rendered,
        context_applied=context,
    )
