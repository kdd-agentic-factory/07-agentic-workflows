# Feature: Document Analysis

Ejemplo de uso de `workflows/create-new-feature.workflow.yaml`.

## Entrada

- `feature_name`: document-analysis
- `user_need`: Extraer entidades, resumen y clasificacion de documentos cargados
  por usuarios.
- `target_repository`: repositorio de aplicacion documental.

## Salidas esperadas

- Brief de feature con alcance y exclusiones.
- Criterios de aceptacion para extraccion, resumen y errores.
- Plan de integracion con el servicio que procesara documentos.
- Informe de validacion con fixtures de documentos representativos.

## Separacion de responsabilidades

Este ejemplo solo define proceso. Los parsers, modelos, endpoints y pruebas de
codigo deben implementarse en el repositorio de producto correspondiente.
