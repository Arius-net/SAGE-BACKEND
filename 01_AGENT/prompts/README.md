# Gobernanza y Versionado de Prompts — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión del esquema:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Prompt activo actual:** `01_AGENT/prompts/active/prompt_activo.md` (`v1.0.0`)

---

## 1. Propósito

Este directorio controla los prompts operativos oficiales empleados para iniciar y alinear sesiones de agentes de IA sobre el repositorio **SAGE**. Su objetivo es asegurar arranque determinista en Fase 0, respeto a las fuentes de autoridad (`00_GOVERNANCE/*` y `DECISION_LOG.md`) y trazabilidad de cambios.

---

## 2. Reglas de Versionado Semántico (SemVer)

Todo prompt operativo sigue **SemVer (`MAYOR.MENOR.PARCHE`)** declarado en su encabezado:

- **MAYOR (`X.0.0`):** cambio en reglas de gobernanza, protocolo de Fase 0, alcance de `DEC-01`/`DEC-02`, incorporación del stack aprobado tras `D02` o modificación de las restricciones obligatorias. Requiere aprobación explícita de Sayd Quevedo.
- **MENOR (`0.Y.0`):** cambio de fase o entregable objetivo (por ejemplo, pasar la preparación de `D01` a `D02`, `D03`, etc.) manteniendo intactas las reglas de gobernanza.
- **PARCHE (`0.0.Z`):** correcciones de redacción, aclaraciones o mejoras de formato sin cambio operativo ni normativo.

---

## 3. Reglas de Control de Versiones de Prompts

1. **Un único prompt activo:** Solo existe un archivo operativo vigente en `01_AGENT/prompts/active/prompt_activo.md`.
2. **Archivo histórico antes de reemplazar:** Cuando se eleve la versión `MAYOR` o `MENOR`, respaldar la versión previa en `01_AGENT/prompts/archive/prompt_vX.Y.Z.md` (creando `archive/` únicamente cuando ocurra la primera transición de versión) antes de actualizar `prompt_activo.md`.
3. **Coherencia con el estado máquina:** El entregable objetivo y las restricciones del prompt activo deben coincidir siempre con `03_MEMORY/state/PROJECT_STATUS.yaml` y `03_MEMORY/state/ACTIVE_TASK.yaml`.
4. **Cero placeholders ni secretos:** Ningún prompt puede contener credenciales, rutas externas privadas ni marcadores incompletos.
