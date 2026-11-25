# Instrucciones de Entrada para Agentes — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo

---

## 1. Primera Acción Obligatoria

Antes de proponer cambios, redactar entregables o escribir código en este repositorio, **todo agente DEBE**:

1. Leer `01_AGENT/01_init.md` completo.
2. Ejecutar íntegramente la **Fase 0 (inspección exclusivamente en solo lectura)** siguiendo `01_AGENT/protocols/phase_0_inspection.md`.
3. Emitir el diagnóstico estructurado de Fase 0 y **detenerse** si no existe autorización explícita del usuario o una tarea autorizada en `03_MEMORY/state/ACTIVE_TASK.yaml` (`authorized: true`).

---

## 2. Fuentes de Autoridad Inmutables

Las siguientes fuentes rigen cualquier interpretación técnica o documental (en orden estricto de precedencia):

1. `03_MEMORY/decisions/DECISION_LOG.md` — Decisiones aprobadas de gobernanza (inmutable, solo anexar; línea base `D-0001`).
2. `00_GOVERNANCE/PROJECT_CHARTER.md` — Alcance, propósito, usuarios y exclusiones de SAGE.
3. `00_GOVERNANCE/DECISION_SPEC.md` — Especificación de `DEC-01` (rebanada vertical) y `DEC-02`, costo del error asimétrico, `data_vintage` y criterios de éxito.
4. `00_GOVERNANCE/WORKING_RULES.md` — Reglas operativas, estados de entregables, reproducibilidad y control de contradicciones.
5. `00_GOVERNANCE/RISK_REGISTER.md` — Riesgos activos y mitigaciones obligatorias.

Si un archivo de contexto (`02_CONTEXT/`) contradice una fuente de gobernanza o `DECISION_LOG.md`, prevalece la fuente de autoridad y el agente debe reportar la discrepancia como `CONTRADICTED`.

---

## 3. Límites Estrictos

- **Stack tecnológico abierto:** Prohibido asumir o introducir lenguajes de programación, librerías de Algoritmos Genéticos, bases de datos o frameworks de interfaz antes de su aprobación formal en `D02`/`D03`.
- **Naturaleza prescriptiva únicamente:** SAGE optimiza rotación de cultivos y riego; prohibido convertirlo en un sistema predictivo de clima o precios.
- **Cero secretos y cero datos sensibles:** Prohibido almacenar credenciales reales, archivos `.env`, datos personales (PII) o datos de salud (PHI).
- **No inventar datos ni resultados:** Prohibido fabricar métricas, gráficas, corridas o evidencia inexistente. Toda afirmación debe llevar trazabilidad y etiqueta epistemológica (`VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN`, `CONTRADICTED`).
- **Inmutabilidad del historial:** Prohibido modificar o borrar asientos existentes en `03_MEMORY/decisions/DECISION_LOG.md`.
- **Evidencia técnica únicamente:** No crear registros de encuestas ni trabajo de campo (no crear `03_MEMORY/evidence/EVIDENCE_REGISTER.csv`).

---

## 4. Contrato Antes de Modificar Archivos

Un agente solo puede pasar a modo de escritura cuando se cumplan **todas** las condiciones siguientes:

1. Fase 0 completada y sin contradicciones críticas abiertas.
2. Existe autorización explícita del responsable (`Sayd Quevedo`) en la sesión actual **o** `03_MEMORY/state/ACTIVE_TASK.yaml` tiene `authorized: true` y `status` distinto de `not_assigned`.
3. El alcance de modificación corresponde exactamente a la tarea o entregable autorizado (`D01`–`D06`) y respeta los límites de `01_AGENT/AGENT_RESTRICTIONS.md`.
4. Cualquier actualización de archivos concluye con verificación de calidad (`01_AGENT/protocols/quality_control.md`) y sincronización de memoria/estado (`01_AGENT/protocols/memory_update.md`).
