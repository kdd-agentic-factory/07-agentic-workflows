"""Test approval gate validation logic."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "validators"))
from validate_approval_gates import validate_approval_gates


def test_passes_when_no_critical_tools():
    workflow = {
        "steps": [{"id": "read_file", "type": "tool", "tool": "filesystem.read"}],
        "approval": {"required": False},
    }
    assert validate_approval_gates(workflow)["passed"] is True


def test_blocks_critical_tool_without_approval():
    workflow = {
        "steps": [{"id": "apply_manifest", "type": "tool", "tool": "kubernetes.apply_manifest"}],
        "approval": {"required": False},
    }
    result = validate_approval_gates(workflow)
    assert result["passed"] is False
    assert "apply_manifest" in result["critical_steps"]


def test_passes_critical_tool_with_approval():
    workflow = {
        "steps": [{"id": "apply_manifest", "type": "tool", "tool": "kubernetes.apply_manifest"}],
        "approval": {"required": True, "approver_role": "platform_owner"},
    }
    assert validate_approval_gates(workflow)["passed"] is True


def test_blocks_rollback_without_approval():
    workflow = {
        "steps": [{"id": "rollback", "type": "tool", "tool": "kubernetes.rollback_deployment"}],
        "approval": {"required": False},
    }
    assert validate_approval_gates(workflow)["passed"] is False


def test_passes_empty_steps():
    workflow = {"steps": [], "approval": {"required": False}}
    assert validate_approval_gates(workflow)["passed"] is True
