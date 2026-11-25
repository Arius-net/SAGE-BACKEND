# Protocolo de Actualización de Memoria y Estado — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Referencia normativa:** `03_MEMORY/MEMORY_POLICY.md`

---

## 1. Disparadores de Actualización

Toda modificación a la capa `03_MEMORY/` y a `02_CONTEXT/CURRENT_STATE.md` ocurre únicamente ante uno de estos disparadores verificados:

| Disparador | Archivos a actualizar | Condición obligatoria |
| :--- | :--- | :--- |
| **Aprobación de decisión de gobernanza o cambio de alcance/stack** | `03_MEMORY/decisions/DECISION_LOG.md` (solo anexar `D-000X`), `03_MEMORY/PROJECT_MEMORY.md`, `02_CONTEXT/DECISION_CONTEXT.md` | Aprobación explícita de Sayd Quevedo. |
| **Inicio, bloqueo, revisión o cierre de un entregable (`D01`–`D06`)** | `03_MEMORY/state/PROJECT_STATUS.yaml`, `03_MEMORY/state/ACTIVE_TASK.yaml`, `02_CONTEXT/CURRENT_STATE.md`, `02_CONTEXT/RESEARCH_CONTEXT.md` | Cumplimiento de `research_execution.md` y `quality_control.md`. |
| **Ejecución de corrida experimental del AG (`D04`/`D05`)** | `03_MEMORY/experiments/EXPERIMENT_LOG.csv` (solo anexar fila) | `seed`, `dataset_version`, `code_version` y `result_path` completos. |
| **Hallazgo técnico, agronómico o error relevante que genera aprendizaje** | `03_MEMORY/lessons_learned/LESSONS.md` (solo anexar `L-000X`) | Etiqueta epistemológica explícita y acción preventiva concreta. |
| **Validación o refutación de supuestos / resolución de preguntas abiertas** | `02_CONTEXT/ASSUMPTIONS.md`, `02_CONTEXT/OPEN_QUESTIONS.md` y `00_GOVERNANCE/RISK_REGISTER.md` (si aplica) | Referencia al entregable o `experiment_id` que soporta el cambio. |

---

## 2. Reglas de Consistencia e Inmutabilidad

1. **Inmutabilidad estricta en `DECISION_LOG.md`:** nunca editar ni borrar `D-0001` ni asientos posteriores; todo cambio se documenta anexando el siguiente ID consecutivo (`D-0002`, `D-0003`, ...).
2. **Separación gobernanza vs. optimización:** jamás registrar planes generados por el AG (`DEC-01`/`DEC-02`) dentro de `DECISION_LOG.md`.
3. **Sincronización atómica de estado:** `PROJECT_STATUS.yaml` y `CURRENT_STATE.md` deben reflejar exactamente la misma fase, el mismo entregable activo y el mismo estado de aprobación al cerrar cualquier iteración.
4. **Limpieza al concluir tarea:** al finalizar una tarea y pasar un entregable a `in_review` o `approved`, restaurar `ACTIVE_TASK.yaml` a un estado seguro (`authorized: false` si no hay una nueva tarea formalmente aprobada).
5. **Validación sintáctica inmediata:** verificar que todo YAML y CSV modificado parsea sin errores antes de concluir la sesión.
