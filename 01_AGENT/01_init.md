# Inicialización Obligatoria del Agente (`01_init.md`) — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo

---

## 1. Regla de Preservación

Toda sesión de agente que ingrese al repositorio de **SAGE** debe preservar intactas las fuentes de autoridad (`00_GOVERNANCE/*`), el registro inmutable (`03_MEMORY/decisions/DECISION_LOG.md`), la separación estricta de capas y el estado del stack tecnológico (**abierto hasta `D02`/`D03`**). Ninguna interpretación informal o suposición del agente puede sobrescribir una decisión aprobada.

---

## 2. Fase 0: Inspección Exclusivamente (7 Pasos Obligatorios)

Antes de ejecutar cualquier modificación, proponer código o abrir entregables, el agente debe completar estos **7 pasos numerados en modo estrictamente de solo lectura**:

1. **Leer las reglas de entrada y operación:** revisar `AGENTS.md`, `01_AGENT/AGENT_INSTRUCTIONS.md` y `01_AGENT/AGENT_RESTRICTIONS.md`.
2. **Verificar la autoridad constitucional del proyecto:** leer `00_GOVERNANCE/PROJECT_CHARTER.md`, `00_GOVERNANCE/DECISION_SPEC.md`, `00_GOVERNANCE/WORKING_RULES.md` y `00_GOVERNANCE/RISK_REGISTER.md`.
3. **Inspeccionar las decisiones inmutables:** leer `03_MEMORY/decisions/DECISION_LOG.md` desde `D-0001` hasta el último asiento registrado.
4. **Comprobar el estado máquina y la autorización activa:** leer `03_MEMORY/state/PROJECT_STATUS.yaml` y `03_MEMORY/state/ACTIVE_TASK.yaml`, verificando explícitamente `current_phase`, `active_deliverable`, `pending_approval` y `authorized`.
5. **Revisar el contexto vigente y contratos técnicos/de datos:** leer `02_CONTEXT/CURRENT_STATE.md`, `02_CONTEXT/DATA_CONTEXT.md`, `02_CONTEXT/TECHNICAL_CONTEXT.md`, `02_CONTEXT/ASSUMPTIONS.md` y `02_CONTEXT/OPEN_QUESTIONS.md`.
6. **Consultar el protocolo de entregables y memoria técnica:** leer `04_RESEARCH/research_protocol.md`, `03_MEMORY/MEMORY_POLICY.md` y comprobar `03_MEMORY/experiments/EXPERIMENT_LOG.csv` y `03_MEMORY/lessons_learned/LESSONS.md`.
7. **Ejecutar verificación cruzada y emitir diagnóstico de Fase 0:** aplicar `01_AGENT/protocols/phase_0_inspection.md`, reportar el estado en los 4 puntos obligatorios y **detenerse** si no existe autorización explícita del responsable (`Sayd Quevedo`) ni `ACTIVE_TASK.yaml` con `authorized: true`.

---

## 3. Prohibiciones Explícitas en Fase 0

Durante la Fase 0 queda **estrictamente prohibido**:

- Crear, modificar, renombrar o eliminar cualquier archivo o directorio del repositorio.
- Crear carpetas futuras (`05_DATA/`, `08_APPLICATION/`, `09_VALIDATION/`, `10_DOCUMENTATION/`, `11_OUTPUTS/`) o abrir entregables en `04_RESEARCH/`.
- Editar `03_MEMORY/state/PROJECT_STATUS.yaml`, `03_MEMORY/state/ACTIVE_TASK.yaml` o agregar asientos en `03_MEMORY/decisions/DECISION_LOG.md`.
- Seleccionar, instalar o asumir un lenguaje de programación, librería de Algoritmos Genéticos, motor de base de datos o framework de interfaz.
- Generar datos sintéticos no autorizados, métricas simuladas o gráficas ficticias.
- Resolver silenciosamente contradicciones documentales (si aparece alguna, etiquetarla como `CONTRADICTED` y detenerse).
