from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_dual_analysis_workflow_enforces_seals_before_confrontation():
    workflow = yaml.safe_load((ROOT / "workflows/race-engineering/dual-analysis.workflow.yaml").read_text())
    assert workflow["workflow_id"] == "dual-analysis"
    steps = workflow["steps"]
    seal = next(i for i, step in enumerate(steps) if step["id"] == "seal_branches")
    confront = next(i for i, step in enumerate(steps) if step["id"] == "confront_sealed_results")
    assert seal < confront
    assert steps[confront]["requires"] == ["principal_sealed", "review_sealed"]
    assert set(workflow["kdd_stages"]) == {"selection", "preprocessing", "transformation", "data_mining", "interpretation"}
    assert set(workflow["specialists"]) == {"chassis", "track", "weather", "physical", "neuro", "tires-powertrain"}
    assert workflow["approval"]["required"] is True
    catalog = yaml.safe_load((ROOT / "catalog/workflows.yaml").read_text(encoding="utf-8"))["workflows"]
    assert next(w for w in catalog if w["id"] == "dual-analysis")["status"] == "proposed"
