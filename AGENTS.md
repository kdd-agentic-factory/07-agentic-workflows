# AGENTS.md

Guia operativa para agentes que trabajen en `07-agentic-workflows`.

## Proposito

Este repositorio contiene logica de proceso: workflows, contratos, ejemplos y
validaciones. No debe absorber implementaciones de producto, conectores pesados,
scripts de despliegue especificos de un cliente ni codigo de dominio que deba
vivir en otro repositorio.

## Reglas de trabajo

- Mantener los workflows declarativos y legibles.
- Preferir contratos explicitos de entrada y salida.
- Documentar decisiones de proceso dentro del workflow, no en codigo externo.
- Mantener ejemplos pequenos, trazables y ejecutables mentalmente.
- Anadir pruebas cuando se cree o cambie la estructura de workflows.
- Evitar secretos, credenciales, rutas locales personales y configuraciones de
  infraestructura real.

## Formato recomendado

Cada workflow debe incluir, como minimo:

- `id`
- `version`
- `description`
- `inputs`
- `outputs`
- `guards`
- `steps`

Los pasos deben expresar responsabilidades, no implementaciones. Un buen paso
dice que artefacto se valida o produce; un mal paso codifica detalles internos
que pertenecen a otro repositorio.

## Criterio de calidad

Un workflow esta listo cuando otra persona puede entender:

1. Que problema resuelve.
2. Que necesita para empezar.
3. Que produce al terminar.
4. Que controles aplican antes de avanzar.
5. Donde se conectaria la logica de codigo externa.
