"""Workflow registry endpoints — list, validate and render KDD workflows."""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Built-in workflow catalog (mirrors the YAML definitions in workflows/ directory)
_WORKFLOWS: Dict[str, Dict[str, Any]] = {
    "pre-grand-prix-preparation": {
        "workflow_id": "pre-grand-prix-preparation",
        "name": "Pre Grand Prix Preparation",
        "description": "Full pre-GP workflow: circuit intelligence, setup proposal, simulation validation",
        "version": "1.0",
        "kdd_stages": ["selection", "preprocessing", "mining", "interpretation"],
        "steps": [
            {"step": "load_circuit_history", "service": "kdd-data-pipelines"},
            {"step": "extract_circuit_patterns", "service": "kdd-data-pipelines"},
            {"step": "build_evidence_packet", "service": "rag-cag"},
            {"step": "generate_setup_proposal", "service": "race-ai-copilot"},
            {"step": "simulate_proposal", "service": "digital-twin", "approval_required": False},
            {"step": "generate_pre_gp_report", "service": "documentation-agent"},
        ],
        "approval_gates": ["setup_proposal"],
        "artifacts": ["circuit_evidence", "setup_proposal", "simulation_result", "pre_gp_report"],
        "triggers": ["manual", "race_calendar_event"],
    },
    "post-session-analysis": {
        "workflow_id": "post-session-analysis",
        "name": "Post Session Analysis",
        "description": "Analyze session telemetry, detect issues, generate crew chief report",
        "version": "1.0",
        "kdd_stages": ["preprocessing", "transformation", "mining", "interpretation"],
        "steps": [
            {"step": "ingest_session_telemetry", "service": "kdd-data-pipelines"},
            {"step": "extract_features", "service": "kdd-data-pipelines"},
            {"step": "detect_patterns", "service": "kdd-data-pipelines"},
            {"step": "build_evidence_packet", "service": "rag-cag"},
            {"step": "generate_crew_chief_report", "service": "documentation-agent"},
        ],
        "approval_gates": [],
        "artifacts": ["session_features", "detected_patterns", "crew_chief_report"],
        "triggers": ["session_completed_event"],
    },
    "tire-degradation-analysis": {
        "workflow_id": "tire-degradation-analysis",
        "name": "Tire Degradation Analysis",
        "description": "KDD analysis of rear tire degradation across laps and corners",
        "version": "1.0",
        "kdd_stages": ["preprocessing", "transformation", "mining"],
        "steps": [
            {"step": "load_tire_telemetry", "service": "kdd-data-pipelines"},
            {"step": "extract_spin_ratio", "service": "kdd-data-pipelines"},
            {"step": "detect_degradation_pattern", "service": "kdd-data-pipelines"},
            {"step": "generate_analysis", "service": "race-ai-copilot"},
        ],
        "approval_gates": [],
        "artifacts": ["tire_features", "degradation_pattern", "analysis_report"],
        "triggers": ["manual", "post_session_event"],
    },
    "setup-change-validation": {
        "workflow_id": "setup-change-validation",
        "name": "Setup Change Validation",
        "description": "Propose, simulate and approve a motorcycle setup change",
        "version": "1.0",
        "kdd_stages": ["interpretation", "deployment"],
        "steps": [
            {"step": "propose_setup_change", "service": "race-ai-copilot"},
            {"step": "simulate_change", "service": "digital-twin"},
            {"step": "request_crew_chief_approval", "service": "security-governance", "approval_required": True},
            {"step": "generate_setup_change_report", "service": "documentation-agent"},
        ],
        "approval_gates": ["crew_chief_approval"],
        "artifacts": ["setup_proposal", "simulation_result", "approval_record", "setup_change_report"],
        "triggers": ["manual", "copilot_recommendation"],
    },
    "paper-section-generation": {
        "workflow_id": "paper-section-generation",
        "name": "Paper Section Generation",
        "description": "Generate an academic paper section from experiment results and evidence",
        "version": "1.0",
        "kdd_stages": ["interpretation"],
        "steps": [
            {"step": "load_experiment_results", "service": "experimentation-lab"},
            {"step": "build_evidence_packet", "service": "rag-cag"},
            {"step": "generate_paper_section", "service": "documentation-agent"},
            {"step": "export_to_latex", "service": "paper-reproducibility-kit"},
        ],
        "approval_gates": [],
        "artifacts": ["evidence_packet", "paper_section", "latex_output"],
        "triggers": ["manual"],
    },
    "dataset-ingestion": {
        "workflow_id": "dataset-ingestion",
        "name": "Dataset Ingestion",
        "description": "Validate, anonymize and ingest a telemetry dataset into the KDD pipeline",
        "version": "1.0",
        "kdd_stages": ["selection", "preprocessing"],
        "steps": [
            {"step": "validate_dataset", "service": "telemetry-dataset"},
            {"step": "anonymize_dataset", "service": "telemetry-dataset"},
            {"step": "export_to_kdd", "service": "telemetry-dataset"},
            {"step": "ingest_telemetry", "service": "kdd-data-pipelines"},
        ],
        "approval_gates": [],
        "artifacts": ["dataset_validation_report", "anonymized_dataset", "ingestion_confirmation"],
        "triggers": ["manual", "new_dataset_event"],
    },
    "simulation-what-if": {
        "workflow_id": "simulation-what-if",
        "name": "Simulation What-If",
        "description": "Run a what-if simulation and generate a simulation report",
        "version": "1.0",
        "kdd_stages": ["interpretation"],
        "steps": [
            {"step": "define_scenario", "service": "race-command-center"},
            {"step": "run_what_if", "service": "digital-twin"},
            {"step": "generate_simulation_report", "service": "documentation-agent"},
        ],
        "approval_gates": [],
        "artifacts": ["scenario_definition", "simulation_result", "simulation_report"],
        "triggers": ["manual"],
    },
    "crew-chief-report-generation": {
        "workflow_id": "crew-chief-report-generation",
        "name": "Crew Chief Report Generation",
        "description": "Generate a complete crew chief decision report with evidence",
        "version": "1.0",
        "kdd_stages": ["interpretation"],
        "steps": [
            {"step": "gather_session_evidence", "service": "rag-cag"},
            {"step": "gather_simulation_results", "service": "digital-twin"},
            {"step": "generate_crew_chief_report", "service": "documentation-agent"},
        ],
        "approval_gates": [],
        "artifacts": ["evidence_packet", "crew_chief_report"],
        "triggers": ["manual", "post_session_event"],
    },
}


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
        for w in _WORKFLOWS.values()
    ]


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    if workflow_id not in _WORKFLOWS:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    return _WORKFLOWS[workflow_id]


@router.get("/{workflow_id}/schema")
async def get_workflow_schema(workflow_id: str):
    if workflow_id not in _WORKFLOWS:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    wf = _WORKFLOWS[workflow_id]
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
    if workflow_id not in _WORKFLOWS:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    rendered = dict(_WORKFLOWS[workflow_id])
    rendered["context"] = context
    return WorkflowRenderResult(
        workflow_id=workflow_id,
        rendered=rendered,
        context_applied=context,
    )
