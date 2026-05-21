# 07-agentic-workflows

Declarative workflow definitions for the KDD-governed agentic race engineering platform.

This repository defines how agents, skills, MCP tools, data pipelines, documentation, dashboards,
simulations and human approvals are coordinated into traceable, versioned and auditable workflows.

---

## What is a workflow?

A workflow is a declarative YAML definition that describes a complete process from inputs to outputs,
including the agents, skills and tools that participate, the approval gates required, and the evidence
that must be generated.

Workflows do not contain business logic. They coordinate decisions, validations and artefacts.
The implementation lives in the services, skills and tools each workflow invokes.

---

## Workflows by category

| Category | Description |
|---|---|
| `governance` | Repository creation, ADR, compliance validation, policy updates |
| `software-engineering` | Feature creation, SDD bundles, pull requests, as-built generation |
| `skills` | Skill creation, validation, AutoSkill detection and promotion |
| `knowledge` | Document ingestion, repository indexing, RAG/CAG cache, evidence export |
| `data` | Telemetry ingestion, cleaning, feature extraction, pattern mining |
| `paper` | Paper section generation, results tables, reproducibility reports |
| `race-engineering` | Pre-GP preparation, FP analysis, qualifying, race strategy, crew chief report |
| `simulation` | What-if setups, engine maps comparison, tire degradation, circuit part evaluation |
| `deployment` | Docker/Kubernetes deploy, rollback, health validation, deployment evidence |
| `observability` | Workflow metrics, logs inspection, failure detection, observability reports |

---

## Workflow structure

Every workflow declares:

```yaml
id:               # stable identifier
name:             # human-readable name
version:          # semver
status:           # proposed | validated | deprecated | disabled
kdd_stage:        # KDD phase this workflow belongs to
description:      # objective of the workflow
inputs:           # required data
outputs:          # produced artefacts
agents:           # agents involved
required_skills:  # skills invoked
required_tools:   # MCP tools used
approval:         # approval gate (required/not, role, reason)
steps:            # ordered execution steps
evidence:         # evidence artefacts that must be produced
metrics:          # observability metrics
```

---

## How to validate workflows

```bash
python validators/validate_workflow_schema.py
python validators/validate_approval_gates.py
python validators/validate_required_artifacts.py
python validators/validate_workflow_catalog.py
python -m pytest tests/
```

Using Make:

```bash
make validate
make test
```

---

## How the orchestrator consumes workflows

The `01-agent-orchestrator` loads workflows from this repository in three ways:

1. **Local filesystem** - reads `workflows/**/*.workflow.yaml` from a mounted volume.
2. **GitHub repository** - reads workflows from the `main` branch at runtime.
3. **RAG/CAG** - retrieves workflow descriptions and examples to explain processes.

Contract:

```
01-agent-orchestrator
    -> load catalog/workflows.yaml
    -> find workflow by id
    -> validate inputs
    -> execute steps
    -> report metrics
```

---

## Approval gates

Critical actions that always require approval:

- Kubernetes deployment
- New repository creation
- AutoSkill promotion
- Setup change recommendation applied to a real car
- Critical race engineering decision
- Policy changes

See [docs/approval-gates.md](docs/approval-gates.md) for the full policy.

---

## Repository role

```
00-kdd-governance     -> defines rules
01-agent-orchestrator -> executes workflows
07-agentic-workflows  -> defines workflows  <- this repository
02-mcp-gateway        -> executes tools
04-skills-autoskills-registry -> executes skills
05-documentation-agent -> generates documentation
06-kdd-data-pipelines  -> processes data
```

---

## Dependencies

| Direction | Repository |
|---|---|
| Depends on | `00-kdd-governance`, `01-agent-orchestrator`, `02-mcp-gateway`, `04-skills-autoskills-registry`, `05-documentation-agent` |
| Used by | `01-agent-orchestrator`, `08-experimentation-lab`, `14-paper-reproducibility-kit`, `15-race-command-center`, `16-race-ai-copilot`, `17-digital-twin-simulation-lab` |
