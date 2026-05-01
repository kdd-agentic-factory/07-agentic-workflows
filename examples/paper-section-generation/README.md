# Paper Section Generation

Ejemplo de uso de `workflows/generate-paper-section.workflow.yaml`.

## Entrada

- `section_name`: Methodology
- `research_question`: Como evaluar workflows agenticos en tareas KDD
  reproducibles.
- `evidence_pack`: notas del experimento, tabla de metricas y referencias
  aprobadas.

## Salidas esperadas

- Esquema argumental de la seccion.
- Borrador con claims trazables a evidencia.
- Lista de citas confirmadas y citas pendientes.
- Notas de revision sobre coherencia, cobertura y limites.

## Separacion de responsabilidades

El workflow no inventa resultados ni sustituye el gestor bibliografico. Su papel
es ordenar el proceso de escritura y revision.
