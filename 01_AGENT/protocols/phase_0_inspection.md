# Protocolo de Fase 0: Inspección Exclusivamente — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Modo de ejecución:** **Solo lectura estricta** (cero escrituras, cero creaciones, cero borrados)

---

## 1. Propósito y Modo Solo Lectura

La Fase 0 garantiza que todo agente que ingrese a una sesión comprenda con exactitud el estado real, las decisiones aprobadas y los límites vigentes de **SAGE** antes de proponer o ejecutar cualquier cambio. Durante toda esta fase el agente opera exclusivamente en modo de lectura.

---

## 2. Lista de Lectura Ordenada

Leer en este orden estricto para construir contexto desde la autoridad hasta el estado operativo:

1. `AGENTS.md` y `01_AGENT/01_init.md`
2. `00_GOVERNANCE/PROJECT_CHARTER.md`
3. `00_GOVERNANCE/DECISION_SPEC.md`
4. `00_GOVERNANCE/WORKING_RULES.md` y `00_GOVERNANCE/RISK_REGISTER.md`
5. `03_MEMORY/decisions/DECISION_LOG.md`
6. `03_MEMORY/state/PROJECT_STATUS.yaml` y `03_MEMORY/state/ACTIVE_TASK.yaml`
7. `02_CONTEXT/CURRENT_STATE.md`, `02_CONTEXT/DATA_CONTEXT.md` y `02_CONTEXT/TECHNICAL_CONTEXT.md`
8. `02_CONTEXT/ASSUMPTIONS.md` y `02_CONTEXT/OPEN_QUESTIONS.md`
9. `04_RESEARCH/research_protocol.md` y `03_MEMORY/MEMORY_POLICY.md`

---

## 3. Verificación de Consistencia Cruzada

Al completar la lectura, comprobar obligatoriamente los seis puntos siguientes:

1. **Identidad y naturaleza:** SAGE está definido en todos los archivos como DSS prescriptivo / optimización por AG (no predictivo), con horizonte de 5 años (10 ciclos `PV`/`OI`) y 3 a 10 parcelas piloto.
2. **Variables y decisiones:** Coinciden las 4 VD (cultivo `0..4`, fecha `PV`/`OI`, riego, parcela), las 4 VO (costo, producción, nitrógeno `N > 0`, desperdicio/estrés hídrico), `DEC-01` (rebanada vertical) y `DEC-02` (Top-3 individuos distintos).
3. **Línea base y fecha:** `D-0001` y la fecha `2026-11-23` son consistentes entre `DECISION_LOG.md`, `PROJECT_STATUS.yaml`, `CURRENT_STATE.md` y `00_GOVERNANCE/*`.
4. **Estado del stack:** `TECHNICAL_CONTEXT.md`, `PROJECT_STATUS.yaml` y `config/environment.example.yaml` confirman el stack abierto hasta `D02`/`D03` (salvo que exista un asiento `D-000X` posterior aprobando `D02`).
5. **Estado de entregables y tarea activa:** `PROJECT_STATUS.yaml` coincide con `CURRENT_STATE.md`, y se verifica si `ACTIVE_TASK.yaml` tiene `authorized: true` o `authorized: false`.
6. **Ausencia de violaciones críticas:** No hay secretos reales, no hay PII/PHI, no hay contradicciones entre fuentes ni archivos faltantes.

---

## 4. Formato de Salida del Diagnóstico (4 Puntos Obligatorios)

Al terminar la inspección, el agente debe responder con exactamente estos cuatro apartados:

    1. Estado actual verificado:
       - Fase actual, entregable activo, último asiento en DECISION_LOG.md y estado de autorización en ACTIVE_TASK.yaml (etiquetado VERIFIED).
    2. Consistencia cruzada y hallazgos:
       - Resultado de los 6 chequeos de consistencia; si hay cualquier discrepancia, listarla explícitamente como CONTRADICTED con rutas afectadas.
    3. Restricciones y riesgos activos relevantes:
       - Estado del stack tecnológico, supuestos vigentes (ASM-01..ASM-05), preguntas abiertas bloqueantes y riesgos prioritarios de RISK_REGISTER.md.
    4. Siguiente acción recomendada y compuerta de autorización:
       - Qué entregable o tarea corresponde ejecutar a continuación y qué aprobación explícita se requiere de Sayd Quevedo antes de escribir.

---

## 5. Regla de Paro

- **Si `ACTIVE_TASK.yaml` tiene `authorized: false` y el usuario no otorgó autorización explícita de escritura:** el agente **DEBE DETENERSE** tras emitir el diagnóstico de 4 puntos y esperar confirmación de Sayd Quevedo.
- **Si se detecta cualquier conflicto etiquetado como `CONTRADICTED`:** el agente **DEBE DETENERSE** incluso si existe una tarea autorizada, hasta que el responsable resuelva la contradicción mediante decisión explícita.
