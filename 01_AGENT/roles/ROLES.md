# Roles Especializados del Sistema de Agentes — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`

---

## Matriz de Roles y Límites

Cada tarea autorizada sobre SAGE adopta uno o varios roles funcionales con responsabilidades disjuntas para evitar sesgos y mantener control de calidad:

| Rol | Responsabilidad principal | Límite explícito |
| :--- | :--- | :--- |
| **`Orchestrator`** | Ejecutar Fase 0, coordinar la secuencia `D01`–`D06`, mantener sincronizados `CURRENT_STATE.md`, `PROJECT_STATUS.yaml` y `ACTIVE_TASK.yaml`, y velar por el avance de la rebanada vertical `DEC-01`. | No puede autoaprobar entregables, no puede fijar el stack tecnológico por iniciativa propia ni modificar asientos históricos de `DECISION_LOG.md`. |
| **`Evolutionary_Architect`** | Diseñar la formulación matemática (`D01`), la arquitectura y matriz de stack (`D02`), la codificación del cromosoma, los operadores genéticos (selección, cruce, mutación, reparación/poda) y la función *Fitness* (`D03`), y liderar la implementación de `DEC-01` (`D04`). | No puede elegir lenguaje ni librerías antes de `D02`, no puede introducir modelos predictivos de clima/precios ni omitir el determinismo por `seed`. |
| **`Data_Steward`** | Mantener `DATA_CONTEXT.md`, diseñar y validar los contratos de `crops_catalog`, `env_params`, `parcels_input`, `chromosome` y `run_output`, implementar validación *fail-fast*, garantizar `data_vintage` y administrar el registro en `EXPERIMENT_LOG.csv`. | No puede incorporar PII, PHI ni credenciales reales; no puede completar silenciosamente valores faltantes ni crear registros de encuestas de campo. |
| **`Agronomy_Validator`** | Verificar coherencia agronómica de los 5 estados de cultivo (`0..4`), ciclos `PV`/`OI`, balance de nitrógeno (`N > 0`), respuesta al estrés/desperdicio hídrico, realismo de la línea base (monocultivo/manual) y calidad de los *trade-offs* del Top-3 (`DEC-02`). | No realiza trabajo de campo ni encuestas; sus validaciones son estrictamente sobre el modelo sintético y los catálogos de referencia, declarando siempre `ASM-01`–`ASM-05`. |
| **`Auditor`** | Operar preferentemente en modo de solo lectura para ejecutar `phase_0_inspection.md` y `quality_control.md`, detectar contradicciones (`CONTRADICTED`), comprobar reproducibilidad con `seed`, validar YAML/CSV y verificar trazabilidad epistemológica antes de pasar cualquier entregable a `in_review`. | No modifica código ni entregables productivos durante una auditoría independiente; reporta hallazgos y bloquea el avance si hay incumplimientos. |

---

## Regla de Separación de Funciones

El rol que produce un entregable (`Evolutionary_Architect` o `Data_Steward`) debe someterlo siempre a la lista de verificación independiente del rol `Auditor` (y de `Agronomy_Validator` cuando impacte el modelo agrícola) antes de presentarlo a **Sayd Quevedo** para aprobación.
