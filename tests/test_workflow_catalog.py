"""Test that all catalog entries resolve to existing files."""
from pathlib import Path
import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
CATALOG_PATH = REPO_ROOT / "catalog" / "workflows.yaml"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_catalog_file_exists():
    assert CATALOG_PATH.exists()


def test_catalog_has_workflows():
    catalog = load_yaml(CATALOG_PATH)
    assert "workflows" in catalog
    assert len(catalog["workflows"]) > 0


def test_all_catalog_entries_have_required_fields():
    catalog = load_yaml(CATALOG_PATH)
    required_fields = {"id", "path", "category", "status", "owner"}
    for entry in catalog["workflows"]:
        missing = required_fields - set(entry.keys())
        assert not missing, f"Entry '{entry.get('id')}' missing fields: {missing}"


def test_all_catalog_paths_exist():
    catalog = load_yaml(CATALOG_PATH)
    missing = [f"{e['id']}: {REPO_ROOT / e['path']}" for e in catalog["workflows"] if not (REPO_ROOT / e["path"]).exists()]
    assert not missing, "Missing workflow files:\n" + "\n".join(missing)


def test_catalog_ids_are_unique():
    catalog = load_yaml(CATALOG_PATH)
    ids = [e["id"] for e in catalog["workflows"]]
    duplicates = [wid for wid in set(ids) if ids.count(wid) > 1]
    assert not duplicates, f"Duplicate IDs: {duplicates}"
