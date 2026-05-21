"""Test that workflow dependency references resolve to known workflow IDs."""
from pathlib import Path
import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def known_ids():
    catalog = load_yaml(REPO_ROOT / "catalog" / "workflows.yaml")
    return {entry["id"] for entry in catalog.get("workflows", [])}


def test_all_dependency_workflow_ids_are_known(known_ids):
    deps = load_yaml(REPO_ROOT / "catalog" / "workflow-dependencies.yaml")
    errors = [f"Unknown: '{d['workflow_id']}'" for d in deps.get("dependencies", []) if d["workflow_id"] not in known_ids]
    assert not errors, "\n".join(errors)


def test_all_depends_on_workflows_are_known(known_ids):
    deps = load_yaml(REPO_ROOT / "catalog" / "workflow-dependencies.yaml")
    errors = []
    for dep in deps.get("dependencies", []):
        for dep_wf in dep.get("depends_on_workflows", []):
            if dep_wf not in known_ids:
                errors.append(f"'{dep['workflow_id']}' depends on unknown '{dep_wf}'")
    assert not errors, "\n".join(errors)
