"""Test evidence artifact validation logic."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "validators"))
from validate_required_artifacts import validate_required_artifacts


def test_passes_when_all_evidence_outputs_declared():
    workflow = {
        "outputs": [{"name": "paper_section", "type": "string"}, {"name": "evidence_packet", "type": "object"}],
        "evidence": {"outputs": ["paper_section", "evidence_packet"]},
    }
    result = validate_required_artifacts(workflow)
    assert result["passed"] is True


def test_fails_when_evidence_output_undeclared():
    workflow = {
        "outputs": [{"name": "paper_section", "type": "string"}],
        "evidence": {"outputs": ["paper_section", "evidence_packet"]},
    }
    result = validate_required_artifacts(workflow)
    assert result["passed"] is False
    assert "evidence_packet" in result["missing"]


def test_passes_with_no_evidence():
    workflow = {"outputs": [{"name": "report", "type": "string"}], "evidence": {}}
    assert validate_required_artifacts(workflow)["passed"] is True
