"""Test that key workflows pass schema validation."""
import pytest
from pathlib import Path
import yaml
from jsonschema import validate, ValidationError

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "workflow.schema.yaml"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def schema():
    return load_yaml(SCHEMA_PATH)


@pytest.mark.parametrize("workflow_path", [
    REPO_ROOT / "workflows/paper/generate-paper-section.workflow.yaml",
    REPO_ROOT / "workflows/software-engineering/create-new-feature.workflow.yaml",
    REPO_ROOT / "workflows/skills/validate-autoskill.workflow.yaml",
    REPO_ROOT / "workflows/deployment/deploy-to-kubernetes.workflow.yaml",
    REPO_ROOT / "workflows/governance/create-new-repository.workflow.yaml",
    REPO_ROOT / "workflows/simulation/run-setup-what-if.workflow.yaml",
    REPO_ROOT / "workflows/race-engineering/pre-grand-prix.workflow.yaml",
])
def test_workflow_passes_schema(workflow_path, schema):
    workflow = load_yaml(workflow_path)
    validate(instance=workflow, schema=schema)


def test_all_workflow_files_pass_schema(schema):
    workflow_files = list((REPO_ROOT / "workflows").rglob("*.workflow.yaml"))
    assert len(workflow_files) > 0, "No workflow files found"
    errors = []
    for wf_path in workflow_files:
        try:
            workflow = load_yaml(wf_path)
            validate(instance=workflow, schema=schema)
        except ValidationError as exc:
            errors.append(f"{wf_path.name}: {exc.message}")
    assert not errors, "Schema validation errors:\n" + "\n".join(errors)
