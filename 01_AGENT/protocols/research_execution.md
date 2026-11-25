# Protocolo de Ejecución de Investigación y Entregables (`D01`–`D06`) — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Referencia maestra:** `04_RESEARCH/research_protocol.md`

---

## 1. Inicio Controlado de un Entregable

Antes de crear cualquier carpeta `04_RESEARCH/D0X_*` o escribir archivos de un entregable, el agente debe confirmar las cuatro compuertas de entrada:

1. **Fase 0 superada sin contradicciones:** diagnóstico completo según `01_AGENT/protocols/phase_0_inspection.md`.
2. **Prerrequisito aprobado:** el entregable previo (`D0(X-1)`) figura como `approved` en `03_MEMORY/state/PROJECT_STATUS.yaml` (para `D01`, el prerrequisito es `D-0001` más autorización `D-0002`).
3. **Tarea autorizada:** `03_MEMORY/state/ACTIVE_TASK.yaml` contiene `authorized: true`, `deliverable: "D0X"`, `inputs`, `expected_outputs`, `acceptance_criteria` y `constraints` explícitos.
4. **Actualización de apertura:** registrar el estado `in_progress` para `D0X` en `PROJECT_STATUS.yaml` y reflejarlo en `02_CONTEXT/CURRENT_STATE.md`.

---

## 2. Priorización Estricta de la Rebanada Vertical `DEC-01`

Durante la secuencia `D01` -> `D04`, toda decisión de diseño e implementación sigue la regla de **rebanada vertical temprana**:

- **`D01` (Formulación y Línea Base):** definir con precisión el modelo matemático/agronómico de las 4 VD y 4 VO, los escenarios piloto (3 a 10 parcelas, 10 ciclos `PV`/`OI`) y el *benchmark* de monocultivo/manual que `DEC-01` debe superar.
- **`D02` (Arquitectura y Matriz de Stack):** seleccionar el stack más simple, transparente y reproducible para implementar `DEC-01` sin sobrediseño; someter la elección a aprobación en `DECISION_LOG.md`.
- **`D03` (Datos, Cromosoma y Fitness):** diseñar contratos *fail-fast* (`crops_catalog`, `env_params`, `parcels_input`, `chromosome`, `run_output`), operadores genéticos válidos y función *Fitness* que proteja `N > 0` y el balance hídrico.
- **`D04` (Implementación Rebanada Vertical `DEC-01`):** cerrar de punta a punta el flujo reproducible con `seed` en `05_DATA/`, `08_APPLICATION/`, `09_VALIDATION/` y `11_OUTPUTS/`, generando la gráfica de convergencia y los **3 mejores individuos distintos** antes de emprender calibraciones extensas.

---

## 3. Calibración, Validación `DEC-02` y Cierre (`D05`–`D06`)

- **`D05` (Calibración, Experimentos y Validación `DEC-02`):** ejecutar corridas multi-semilla y análisis de sensibilidad registrados en `03_MEMORY/experiments/EXPERIMENT_LOG.csv`, demostrar mejora robusta frente a la línea base y validar la calidad comparativa de los *trade-offs* del Top-3 (`DEC-02`).
- **`D06` (Documentación Final y Defensa Académica):** consolidar manuales reproducibles en `10_DOCUMENTATION/`, auditar trazabilidad completa y preparar el paquete final de entrega para *Fundamentos de Inteligencia Artificial*.

---

## 4. Cierre Formal de Cada Entregable

Un entregable `D0X` solo puede pasar de `in_progress` a `in_review` (y luego a `approved` por Sayd Quevedo) cuando:

1. Su carpeta `04_RESEARCH/D0X_<nombre>/` contiene al menos `README.md`, `01_SPEC.md` y `02_VERIFICATION.md` completos y sin placeholders.
2. Supera íntegramente `01_AGENT/protocols/quality_control.md`.
3. Toda evidencia técnica generada cumple `01_AGENT/protocols/evidence_collection.md`.
4. Se actualizan `PROJECT_STATUS.yaml`, `CURRENT_STATE.md` y (al aprobarse decisiones estructurales) se anexa un nuevo asiento en `DECISION_LOG.md`, cerrando `ACTIVE_TASK.yaml` con `authorized: false`.
