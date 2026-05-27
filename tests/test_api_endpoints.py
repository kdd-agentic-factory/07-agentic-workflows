"""API endpoint integration tests for the workflow registry service."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="module")
def client():
    import workflow_registry.routers.workflows as wf_mod
    from workflow_registry.services.workflow_service import WorkflowService

    wf_mod._service = WorkflowService(root=str(REPO_ROOT))

    from workflow_registry.main import create_app
    app = create_app()
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "workflow-registry-service"


def test_metrics_endpoint(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Workflows — list
# ---------------------------------------------------------------------------

def test_list_workflows(client):
    resp = client.get("/api/v1/workflows")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_list_workflows_schema(client):
    resp = client.get("/api/v1/workflows")
    wf = resp.json()[0]
    assert "workflow_id" in wf
    assert "name" in wf
    assert "description" in wf
    assert "version" in wf
    assert "triggers" in wf


def test_list_workflows_contains_governance(client):
    resp = client.get("/api/v1/workflows")
    ids = [w["workflow_id"] for w in resp.json()]
    assert "create-new-repository" in ids


def test_list_workflows_contains_race_engineering(client):
    resp = client.get("/api/v1/workflows")
    ids = [w["workflow_id"] for w in resp.json()]
    assert any("grand-prix" in wid or "race" in wid for wid in ids)


# ---------------------------------------------------------------------------
# Workflows — get by id
# ---------------------------------------------------------------------------

def test_get_workflow_found(client):
    resp = client.get("/api/v1/workflows/create-new-repository")
    assert resp.status_code == 200
    data = resp.json()
    assert data["workflow_id"] == "create-new-repository"
    assert "steps" in data
    assert "kdd_stages" in data


def test_get_workflow_not_found(client):
    resp = client.get("/api/v1/workflows/nonexistent-workflow-xyz")
    assert resp.status_code == 404


def test_get_workflow_has_full_fields(client):
    resp = client.get("/api/v1/workflows/create-new-repository")
    data = resp.json()
    assert "approval_gates" in data
    assert "artifacts" in data
    assert "triggers" in data
    assert "status" in data
    assert "category" in data


# ---------------------------------------------------------------------------
# Workflows — schema endpoint
# ---------------------------------------------------------------------------

def test_get_workflow_schema(client):
    resp = client.get("/api/v1/workflows/create-new-repository/schema")
    assert resp.status_code == 200
    data = resp.json()
    assert data["workflow_id"] == "create-new-repository"
    assert "steps" in data
    assert "approval_gates" in data
    assert "artifacts" in data
    assert "kdd_stages" in data


def test_get_workflow_schema_not_found(client):
    resp = client.get("/api/v1/workflows/no-such-workflow/schema")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Workflows — validate
# ---------------------------------------------------------------------------

def test_validate_workflow_valid(client):
    resp = client.post("/api/v1/workflows/validate", json={
        "workflow_id": "my-test-wf",
        "steps": [{"step": "do_thing"}],
        "kdd_stages": ["mining"],
        "approval_gates": [],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert data["errors"] == []


def test_validate_workflow_missing_steps(client):
    resp = client.post("/api/v1/workflows/validate", json={
        "workflow_id": "bad-wf",
        "kdd_stages": ["mining"],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is False
    assert any("steps" in e.lower() for e in data["errors"])


def test_validate_workflow_missing_kdd_stages_warns(client):
    resp = client.post("/api/v1/workflows/validate", json={
        "workflow_id": "partial-wf",
        "steps": [{"step": "do_thing"}],
        "approval_gates": [],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert any("kdd_stages" in w for w in data["warnings"])


# ---------------------------------------------------------------------------
# Workflows — render
# ---------------------------------------------------------------------------

def test_render_workflow(client):
    resp = client.post(
        "/api/v1/workflows/render",
        params={"workflow_id": "create-new-repository"},
        json={"rider": "MM93", "circuit": "jerez"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["workflow_id"] == "create-new-repository"
    assert "rendered" in data
    assert data["context_applied"] == {"rider": "MM93", "circuit": "jerez"}


def test_render_workflow_not_found(client):
    resp = client.post(
        "/api/v1/workflows/render",
        params={"workflow_id": "no-such-workflow"},
        json={},
    )
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# WorkflowService — unit
# ---------------------------------------------------------------------------

def test_workflow_service_count():
    from workflow_registry.services.workflow_service import WorkflowService
    svc = WorkflowService(root=str(REPO_ROOT))
    assert svc.count() > 10


def test_workflow_service_categories():
    from workflow_registry.services.workflow_service import WorkflowService
    svc = WorkflowService(root=str(REPO_ROOT))
    cats = svc.categories()
    assert "governance" in cats
    assert isinstance(cats, list)
    assert cats == sorted(cats)


def test_workflow_service_get_missing_returns_none():
    from workflow_registry.services.workflow_service import WorkflowService
    svc = WorkflowService(root=str(REPO_ROOT))
    assert svc.get("does-not-exist") is None
