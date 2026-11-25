# Restricciones del Agente — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo

---

## 1. Prohibiciones Absolutas

Las siguientes acciones están **prohibidas en toda circunstancia**, incluso bajo tarea autorizada:

1. **Omitir la Fase 0:** nunca escribir archivos antes de inspeccionar en solo lectura `AGENTS.md`, `01_AGENT/01_init.md`, `03_MEMORY/decisions/DECISION_LOG.md` y `03_MEMORY/state/*.yaml`.
2. **Sobrescribir o borrar asientos en `DECISION_LOG.md`:** el registro de decisiones es estrictamente inmutable (*append-only*).
3. **Asumir el stack tecnológico antes de `D02`:** prohibido introducir lenguajes, librerías de AG, motores de base de datos o frameworks de interfaz como hechos consumados antes de su aprobación formal.
4. **Introducir capacidades predictivas:** prohibido agregar pronósticos climáticos, series de tiempo de precios o modelos predictivos ajenos al enfoque DSS prescriptivo de SAGE.
5. **Exponer o almacenar datos sensibles o secretos:** cero PII, cero PHI, cero credenciales reales y cero versionado de archivos `.env`.
6. **Fabricar evidencia o usar marcadores incompletos:** prohibido inventar corridas, métricas, gráficas o resultados, así como dejar placeholders (`TODO`, `[completar]`) en entregables o documentación.
7. **Crear registro de evidencia de campo:** prohibido crear `03_MEMORY/evidence/EVIDENCE_REGISTER.csv`, ya que SAGE maneja exclusivamente evidencia técnica.
8. **Resolver contradicciones en silencio:** ante cualquier conflicto entre archivos, detenerse y reportarlo como `CONTRADICTED`.
9. **Ocultar fallos parciales:** prohibido silenciar catálogos inválidos, restricciones violadas (`N <= 0`) o fallos en la generación de gráficas/tablas obligatorias.

---

## 2. Acciones que Requieren Autorización Explícita Previa

El agente debe solicitar y recibir aprobación explícita de **Sayd Quevedo** (reflejada en `ACTIVE_TASK.yaml` o en instrucción directa verificable) antes de:

- Iniciar cualquier entregable de `04_RESEARCH/` (`D01`–`D06`) o cambiar su estado en `PROJECT_STATUS.yaml`.
- Registrar un nuevo asiento (`D-0002+`) en `03_MEMORY/decisions/DECISION_LOG.md`.
- Modificar `00_GOVERNANCE/*` o elevar la versión SemVer de `01_AGENT/prompts/active/prompt_activo.md`.
- Crear la estructura ejecutable en `05_DATA/`, `08_APPLICATION/`, `09_VALIDATION/`, `10_DOCUMENTATION/` o `11_OUTPUTS/`.
- Cambiar parámetros globales del modelo piloto (número de parcelas fuera de `3..10`, horizonte distinto de `10` ciclos `PV`/`OI` o alteración de los 5 códigos de cultivo `0..4`).
