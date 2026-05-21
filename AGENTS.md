# AGENTS.md - Agentic Workflows

## Repository Mission

This repository defines declarative workflows for the KDD-governed agentic race engineering platform.
It coordinates agents, skills, MCP tools, data pipelines, documentation, simulations and human
approvals into traceable, versioned and auditable processes.

---

## Mandatory Rules

- Do not implement business logic in workflow files.
- Do not define workflows without `kdd_stage`.
- Do not define workflows without `inputs` and `outputs`.
- Do not call unregistered skills.
- Do not call unregistered MCP tools.
- Do not omit approval gates for critical actions.
- Do not create race engineering action workflows without evidence requirements.
- Do not create deployment workflows without rollback and health validation.
- Do not merge a workflow with `status: proposed` directly to production use.
- Do not reference credentials, secrets or personal local paths in workflows.

---

## Allowed Responsibilities

- Define workflows in YAML.
- Version workflows using semver.
- Document workflow intent and rationale.
- Declare agents, skills and tools per workflow.
- Declare approval gates per workflow.
- Declare evidence outputs per workflow.
- Define observability metrics per workflow.
- Validate workflow schema, dependencies and catalog.
- Maintain catalog and maturity files.

---

## Forbidden Responsibilities

- Executing workflows directly.
- Implementing algorithms or domain logic.
- Writing production application code.
- Deploying infrastructure.
- Generating final documents or reports.
- Training or fine-tuning models.
- Managing secrets or credentials.

---

## Workflow Quality Criteria

A workflow is ready when another agent or engineer can answer:

1. What problem does this solve?
2. What inputs does it need to start?
3. What outputs does it produce when complete?
4. What controls apply before advancing?
5. Who must approve critical steps?
6. What evidence must be recorded?
7. Which KDD stage does this represent?

---

## Workflow Format

Every workflow must include at minimum:

```yaml
id:
name:
version:
status:
kdd_stage:
description:
inputs:
outputs:
agents:
required_skills:
required_tools:
approval:
steps:
evidence:
metrics:
```

---

## KDD Stage Mapping

| Stage | When to use |
|---|---|
| `selection` | Workflows that select data, sessions or repositories to process |
| `preprocessing` | Workflows that clean, filter or normalise data |
| `transformation` | Workflows that extract features or build representations |
| `data_mining` | Workflows that run pattern mining, clustering or prediction |
| `interpretation` | Workflows that generate insights, recommendations or decisions |
| `documentation` | Workflows that generate artefacts, reports or specifications |
| `deployment` | Workflows that deploy, configure or decommission services |

---

## Approval Gate Policy

A workflow must set `approval.required: true` when it:

- Creates or deletes a repository.
- Promotes an AutoSkill to validated status.
- Applies a setup change recommendation to a physical or simulated car.
- Deploys to Kubernetes or any production environment.
- Modifies governance policy.
- Makes a critical race engineering decision.

---

## Step Types

| Type | Description |
|---|---|
| `agent` | Invokes an agent action |
| `skill` | Invokes a registered skill |
| `tool` | Invokes an MCP tool |
| `approval` | Pauses for human approval |

---

## Agents Reference

| Agent | Role |
|---|---|
| `planner_agent` | Decomposes goals and orchestrates multi-step work |
| `architect_agent` | Validates architectural boundaries and decisions |
| `builder_agent` | Coordinates implementation tasks |
| `reviewer_agent` | Validates outputs and enforces quality gates |
| `documentation_agent` | Generates and validates documentation artefacts |
| `kdd_admin_agent` | Enforces KDD governance and evidence requirements |
| `simulation_agent` | Coordinates simulation and what-if analysis |
| `crew_chief_agent` | Generates race engineering decisions and reports |
