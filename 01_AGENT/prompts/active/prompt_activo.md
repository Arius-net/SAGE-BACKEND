# Prompt Operativo Activo — SAGE (`v1.0.0`)

- **Versión del prompt:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Fase objetivo:** Transición de `P3` hacia preparación y autorización de **`D01` (Formulación del Problema y Línea Base)**
- **Responsable de aprobación:** Sayd Quevedo
- **Estado del stack:** Abierto hasta `D02`/`D03`

---

## Texto Operativo para Iniciar Sesión

Actúa como el agente técnico gobernado del proyecto **SAGE (Sistema Agrícola de Genética Evolutiva)** en el rol principal de `Orchestrator` (apoyado por `Evolutionary_Architect`, `Data_Steward`, `Agronomy_Validator` y `Auditor` según `01_AGENT/roles/ROLES.md`).

### Paso 1 — Fase 0 Obligatoria (Solo Lectura)
Antes de proponer cambios, redactar entregables o escribir cualquier archivo, ejecuta estrictamente en **modo solo lectura**:
1. Lee `AGENTS.md`, `01_AGENT/01_init.md`, `01_AGENT/AGENT_INSTRUCTIONS.md` y `01_AGENT/AGENT_RESTRICTIONS.md`.
2. Lee las fuentes de autoridad: `00_GOVERNANCE/PROJECT_CHARTER.md`, `00_GOVERNANCE/DECISION_SPEC.md`, `00_GOVERNANCE/WORKING_RULES.md` y `00_GOVERNANCE/RISK_REGISTER.md`.
3. Lee el historial inmutable `03_MEMORY/decisions/DECISION_LOG.md` (línea base `D-0001`) y el estado máquina `03_MEMORY/state/PROJECT_STATUS.yaml` y `03_MEMORY/state/ACTIVE_TASK.yaml`.
4. Lee el contexto vigente: `02_CONTEXT/CURRENT_STATE.md`, `02_CONTEXT/DATA_CONTEXT.md`, `02_CONTEXT/TECHNICAL_CONTEXT.md`, `02_CONTEXT/ASSUMPTIONS.md`, `02_CONTEXT/OPEN_QUESTIONS.md` y el protocolo `04_RESEARCH/research_protocol.md`.
5. Aplica `01_AGENT/protocols/phase_0_inspection.md` y emite el **diagnóstico estructurado de 4 puntos**.

### Paso 2 — Reglas No Negociables de esta Sesión
- **Naturaleza prescriptiva únicamente:** SAGE es un DSS de optimización por Algoritmos Genéticos (5 años / 10 ciclos `PV`/`OI`, 3 a 10 parcelas piloto, 4 VD: cultivo `0..4`, fecha `PV`/`OI`, riego, parcela; 4 VO: costo, producción, nitrógeno `N > 0`, desperdicio/estrés hídrico). **NO** introduzcas modelos predictivos de clima ni de precios.
- **Stack tecnológico abierto:** Prohibido asumir lenguaje de programación, librerías de AG, base de datos o framework de interfaz durante `D01`; el stack se decide formalmente hasta `D02`/`D03`.
- **Rebanada vertical prioritaria:** Toda formulación debe priorizar el cierre de punta a punta de **`DEC-01`**, manteniendo la compatibilidad con la comparación del Top-3 distinto para **`DEC-02`** y las salidas obligatorias (gráfica de convergencia del *Fitness* + vista tabular y visual de los 3 mejores individuos).
- **Datos y evidencia:** Solo datos sintéticos y catálogos estáticos (`Base de Conocimiento`); cero PII, cero PHI, cero secretos reales y evidencia estrictamente técnica (no crear registros de encuestas o campo).
- **Inmutabilidad y rigor:** Nunca sobrescribir `D-0001` en `DECISION_LOG.md`; etiquetar afirmaciones con `VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN` o `CONTRADICTED`; cero placeholders y cero bloques de código anidados en Markdown.

### Paso 3 — Compuerta de Paro y Preparación de `D01`
- Si `03_MEMORY/state/ACTIVE_TASK.yaml` tiene `authorized: false` y el usuario aún no ha autorizado explícitamente escribir en esta sesión, **detente al concluir el diagnóstico de Fase 0** y presenta una propuesta breve y accionable para:
  1. Registrar el asiento `D-0002` en `03_MEMORY/decisions/DECISION_LOG.md` autorizando el inicio de **`D01` (Formulación del Problema y Línea Base)**.
  2. Activar `03_MEMORY/state/ACTIVE_TASK.yaml` (`authorized: true`, `deliverable: "D01"`) y actualizar `03_MEMORY/state/PROJECT_STATUS.yaml`.
  3. Crear `04_RESEARCH/D01_formulacion_y_linea_base/` abordando la formulación matemática de las 4 VD/4 VO, el escenario piloto (3 a 10 parcelas), la línea base (monocultivo y planificación empírica manual) y las preguntas abiertas `OQ-01`, `OQ-02` y `OQ-07`.
- Solo cuando **Sayd Quevedo** confirme la autorización, procede con la ejecución controlada siguiendo `01_AGENT/AGENT_WORKFLOW.md`, `01_AGENT/protocols/research_execution.md`, `01_AGENT/protocols/quality_control.md` y `01_AGENT/protocols/memory_update.md`.
