# 07-agentic-workflows

Repositorio de flujos completos para orquestar trabajo agentico de extremo a extremo.

Este repositorio separa la logica de proceso de la logica de codigo: aqui se
definen workflows, contratos, ejemplos y validaciones; la implementacion concreta
vive en los repositorios o skills que cada flujo invoca.

## Estructura

```text
07-agentic-workflows/
|-- README.md
|-- AGENTS.md
|-- workflows/
|   |-- create-new-repository.workflow.yaml
|   |-- create-new-feature.workflow.yaml
|   |-- create-new-skill.workflow.yaml
|   |-- validate-autoskill.workflow.yaml
|   |-- generate-paper-section.workflow.yaml
|   |-- run-kdd-experiment.workflow.yaml
|   |-- deploy-to-docker.workflow.yaml
|   `-- deploy-to-kubernetes.workflow.yaml
|-- examples/
|   |-- feature-document-analysis/
|   |-- feature-telemetry-anomaly/
|   `-- paper-section-generation/
`-- tests/
```

## Convenciones de workflow

Cada archivo `*.workflow.yaml` describe un proceso reusable con:

- `id`: identificador estable del workflow.
- `version`: version del contrato del workflow.
- `description`: objetivo del flujo.
- `inputs`: datos que debe aportar el usuario, agente o sistema externo.
- `outputs`: artefactos producidos por el flujo.
- `guards`: condiciones de entrada, calidad y seguridad.
- `steps`: pasos de proceso, cada uno con rol, accion y entregables.

Los workflows no deben contener logica de negocio embebida ni codigo de producto.
Su funcion es coordinar decisiones, validaciones y artefactos.

## Ejemplos

Los ejemplos muestran como aplicar los workflows sin acoplarlos a una
implementacion concreta:

- `examples/feature-document-analysis`: alta de una feature de analisis documental.
- `examples/feature-telemetry-anomaly`: alta de una feature de deteccion de anomalias.
- `examples/paper-section-generation`: generacion de una seccion academica.

## Validacion

Las pruebas de `tests/` comprueban que la arquitectura esperada existe y que los
workflows conservan las claves de contrato minimas.

```powershell
python -m pytest
```
