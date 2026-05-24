"""WorkflowService — loads workflow definitions from on-disk YAML catalog."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


def _load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _normalize(raw: dict, catalog_entry: dict) -> Dict[str, Any]:
    """Normalize on-disk YAML schema → unified API dict."""
    wf_id = raw.get("id") or catalog_entry.get("id", "unknown")

    # kdd_stages — may be a string or list
    kdd = raw.get("kdd_stages") or raw.get("kdd_stage", "")
    if isinstance(kdd, str) and kdd:
        kdd = [kdd]
    elif not kdd:
        kdd = []

    # steps — normalize heterogeneous schemas
    steps_raw = raw.get("steps", [])
    steps = []
    for s in steps_raw:
        if isinstance(s, dict):
            steps.append({
                "step": s.get("id") or s.get("step") or s.get("action", ""),
                "role": s.get("role", ""),
                "service": s.get("service", ""),
                "approval_required": s.get("approval_required", False),
                "produces": s.get("produces", []),
            })
        elif isinstance(s, str):
            steps.append({"step": s})

    # approval_gates / guards
    approval_gates = raw.get("approval_gates") or []
    guards = raw.get("guards") or []
    if isinstance(guards, list) and guards and not approval_gates:
        approval_gates = [str(g) for g in guards]

    # artifacts from outputs
    outputs_raw = raw.get("outputs", [])
    artifacts: List[str] = []
    for o in outputs_raw:
        if isinstance(o, dict):
            artifacts.append(o.get("name", str(o)))
        elif isinstance(o, str):
            artifacts.append(o)

    # triggers
    triggers = raw.get("triggers", ["manual"])
    if isinstance(triggers, str):
        triggers = [triggers]

    return {
        "workflow_id": wf_id,
        "name": raw.get("name") or wf_id.replace("-", " ").title(),
        "description": raw.get("description", ""),
        "version": str(raw.get("version", "1.0")),
        "status": raw.get("status") or catalog_entry.get("status", "proposed"),
        "category": catalog_entry.get("category", ""),
        "owner": catalog_entry.get("owner", ""),
        "kdd_stages": kdd,
        "steps": steps,
        "approval_gates": approval_gates,
        "artifacts": artifacts,
        "triggers": triggers,
        "inputs": raw.get("inputs", []),
        "agents": raw.get("agents", []),
        "required_skills": raw.get("required_skills", []),
        "target_repositories": raw.get("target_repositories", []),
    }


class WorkflowService:
    """Loads and serves workflow definitions from YAML files on disk.

    Falls back to an empty catalog gracefully if the root directory is absent.
    """

    def __init__(self, root: Optional[str] = None) -> None:
        self._root = Path(root or os.getenv("WORKFLOWS_ROOT", ".")).resolve()
        self._catalog_path = self._root / "catalog" / "workflows.yaml"
        self._workflows: Dict[str, Dict[str, Any]] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        if not self._catalog_path.exists():
            logger.warning("Workflow catalog not found at %s — serving empty catalog", self._catalog_path)
            return
        try:
            catalog = _load_yaml(self._catalog_path)
            entries = catalog.get("workflows", [])
        except Exception as exc:
            logger.error("Failed to load workflow catalog: %s", exc)
            return

        for entry in entries:
            wf_id = entry.get("id", "")
            rel_path = entry.get("path", "")
            if not wf_id or not rel_path:
                continue
            yaml_path = self._root / rel_path
            if not yaml_path.exists():
                logger.debug("Workflow YAML not found: %s", yaml_path)
                continue
            try:
                raw = _load_yaml(yaml_path)
                self._workflows[wf_id] = _normalize(raw, entry)
            except Exception as exc:
                logger.warning("Failed to load workflow '%s': %s", wf_id, exc)

        logger.info("WorkflowService loaded %d workflows from %s", len(self._workflows), self._root)

    def list(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return list(self._workflows.values())

    def get(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        self._ensure_loaded()
        return self._workflows.get(workflow_id)

    def count(self) -> int:
        self._ensure_loaded()
        return len(self._workflows)

    def categories(self) -> List[str]:
        self._ensure_loaded()
        return sorted({w.get("category", "") for w in self._workflows.values() if w.get("category")})
