# Política de Memoria, Contexto y Estado — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo

---

## 1. Separación Estricta: Contexto vs. Memoria vs. Estado

Para evitar duplicación, derivas documentales y pérdidas de trazabilidad entre sesiones de agentes, SAGE separa estrictamente tres planos:

1. **Contexto (`02_CONTEXT/`):** vista compacta, vigente y navegable del proyecto. Enlaza a las fuentes canónicas de gobernanza y memoria sin reescribirlas ni duplicar normativa.
2. **Memoria (`03_MEMORY/`):** registro histórico y consolidado de decisiones de gobernanza (`DECISION_LOG.md`), corridas experimentales (`EXPERIMENT_LOG.csv`), aprendizajes (`LESSONS.md`) y síntesis estable (`PROJECT_MEMORY.md`).
3. **Estado operativo (`03_MEMORY/state/`):** instantánea estructurada en YAML (`PROJECT_STATUS.yaml` y `ACTIVE_TASK.yaml`) legible por máquina para controlar fase, entregables, autorización y restricciones de ejecución.

> **Nota sobre evidencia:** SAGE utiliza únicamente evidencia técnica (código, corridas con `seed`, pruebas, métricas y gráficas). Por decisión `D-0001`, no realiza encuestas ni trabajo de campo y no mantiene registros de evidencia cualitativa de campo.

---

## 2. Tabla de Capas de Memoria

| Artefacto | Ruta | Tipo de contenido | Política de escritura |
| :--- | :--- | :--- | :--- |
| **Registro de decisiones** | `03_MEMORY/decisions/DECISION_LOG.md` | Decisiones formales de gobernanza, alcance, arquitectura y stack (`D-0001`, `D-0002`, ...) | **Solo anexar (inmutable).** Jamás sobrescribir ni borrar asientos previos. |
| **Bitácora de experimentos** | `03_MEMORY/experiments/EXPERIMENT_LOG.csv` | Corridas reproducibles del AG con `seed`, versión de datos, código, parámetros y métricas | **Solo anexar.** Cada corrida nueva agrega una fila con `experiment_id` único. |
| **Lecciones aprendidas** | `03_MEMORY/lessons_learned/LESSONS.md` | Hallazgos técnicos, agronómicos o metodológicos con impacto reutilizable (`L-0001`, ...) | **Solo anexar cronológicamente.** |
| **Memoria consolidada** | `03_MEMORY/PROJECT_MEMORY.md` | Síntesis de identidad, decisiones aprobadas, restricciones persistentes y referencias clave | Actualizable al cerrar hitos o aprobar nuevos asientos en `DECISION_LOG.md`. |
| **Estado del proyecto** | `03_MEMORY/state/PROJECT_STATUS.yaml` | Fase actual, estado de `D01`–`D06`, última validación y bandera de aprobación pendiente | Actualizable únicamente tras cambios verificados de fase o entregable. |
| **Tarea activa** | `03_MEMORY/state/ACTIVE_TASK.yaml` | Contrato ejecutable de la tarea en curso (`authorized`, entradas, salidas y restricciones) | Actualizable solo con autorización explícita del responsable de aprobación. |

---

## 3. Reglas de Actualización e Inmutabilidad

1. **Inmutabilidad absoluta de `DECISION_LOG.md`:** Si una decisión posterior modifica o revoca una anterior, se agrega un nuevo asiento (`D-000X`) que referencia explícitamente el ID anterior y declara su reemplazo; nunca se edita el asiento histórico.
2. **Separación entre decisiones de gobernanza y salidas del AG:** Los planes agrícolas generados por el Algoritmo Genético (Top-3 individuos para `DEC-01`/`DEC-02`) **nunca** se registran en `DECISION_LOG.md`; pertenecen a `EXPERIMENT_LOG.csv` y a `11_OUTPUTS/`.
3. **Sincronización obligatoria tras hitos:** Todo cambio en `PROJECT_STATUS.yaml` debe reflejarse en la misma iteración en `02_CONTEXT/CURRENT_STATE.md` y, cuando corresponda, en `03_MEMORY/PROJECT_MEMORY.md`.
4. **Etiquetado epistemológico obligatorio:** Toda afirmación persistida en memoria o contexto debe clasificarse como `VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN` o `CONTRADICTED`.
5. **Reproducibilidad en experimentos:** Ninguna fila en `EXPERIMENT_LOG.csv` es válida si omite `dataset_version`, `code_version`, `parameters` (incluyendo `seed`) o `result_path`.
6. **Validación sintáctica antes de cerrar:** Cualquier edición a archivos YAML o CSV de `03_MEMORY/` debe superar validación sintáctica antes de dar por concluida la tarea.
