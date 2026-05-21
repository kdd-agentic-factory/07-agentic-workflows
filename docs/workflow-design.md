# Workflow Design

## Structure

| Field | Required | Description |
|---|---|---|
| `id` | yes | Stable kebab-case identifier |
| `name` | yes | Human-readable name |
| `version` | yes | Semver MAJOR.MINOR.PATCH |
| `status` | yes | proposed / validated / active / deprecated / disabled |
| `kdd_stage` | yes | KDD process stage |
| `description` | yes | Objective |
| `inputs` | yes | Required data |
| `outputs` | yes | Artefacts produced |
| `agents` | no | Agents that participate |
| `required_skills` | no | Skills invoked |
| `required_tools` | no | MCP tools used |
| `approval` | no | Approval gate |
| `steps` | yes | Execution steps |
| `evidence` | no | Evidence outputs required |
| `metrics` | no | Observability metrics |

## Step types

| Type | Description |
|---|---|
| `agent` | Invokes an agent with an action |
| `skill` | Invokes a registered skill |
| `tool` | Invokes an MCP tool |
| `approval` | Pauses execution for human decision |

## KDD stage mapping

| Stage | Workflows |
|---|---|
| `selection` | Ingestion, indexing, collection |
| `preprocessing` | Cleaning, normalisation, filtering |
| `transformation` | Feature extraction, caching |
| `data_mining` | Pattern mining, prediction, clustering |
| `interpretation` | Analysis, recommendations, strategy |
| `documentation` | Report generation, paper sections, specs |
| `deployment` | Deploy, rollback, health validation |
