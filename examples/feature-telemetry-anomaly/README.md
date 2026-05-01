# Feature: Telemetry Anomaly

Ejemplo de uso de `workflows/create-new-feature.workflow.yaml`.

## Entrada

- `feature_name`: telemetry-anomaly
- `user_need`: Detectar desviaciones en metricas de servicios y priorizar
  alertas accionables.
- `target_repository`: repositorio de observabilidad o plataforma MLOps.

## Salidas esperadas

- Brief con metricas objetivo, ventanas temporales y consumidores.
- Criterios de aceptacion para precision, latencia y explicabilidad minima.
- Plan de integracion con fuentes de telemetria y canales de alerta.
- Informe de validacion con escenarios normales, degradados y anomalos.

## Separacion de responsabilidades

El workflow no decide el algoritmo ni el backend de series temporales. Solo
coordina las decisiones y evidencias necesarias para implementar la feature.
