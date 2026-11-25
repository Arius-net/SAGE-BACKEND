# Instrucciones Operativas del Agente — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo

---

## 1. Cinco Principios Operativos

1. **Decisión primero:** Todo análisis, dato, métrica o módulo debe vincularse directamente a `DEC-01` (planificación espaciotemporal de rotación y riego) o `DEC-02` (selección entre los 3 mejores individuos distintos). Si no apoya una decisión declarada, no se construye.
2. **Primero inspeccionar:** Toda sesión inicia en solo lectura ejecutando los 7 pasos de `01_AGENT/01_init.md` y el protocolo `01_AGENT/protocols/phase_0_inspection.md`.
3. **Evidencia explícita:** Toda afirmación técnica debe respaldarse con código, pruebas, corridas reproducibles con `seed` o referencias canónicas, y clasificarse con su etiqueta epistemológica (`VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN`, `CONTRADICTED`).
4. **Frescura e incertidumbre siempre visibles:** Toda propuesta o salida debe declarar `data_vintage`, supuestos aplicables (`ASM-01`–`ASM-05`), parámetros estáticos y comparación contra la línea base (monocultivo / planificación empírica manual).
5. **Trazabilidad completa:** Ninguna modificación se da por cerrada sin superar control de calidad (`quality_control.md`) y sincronizar estado y memoria (`memory_update.md`).

---

## 2. Ciclo de Trabajo de 11 Pasos

1. **Ejecutar Fase 0 (solo lectura):** leer fuentes de autoridad, estado y contexto según `01_AGENT/01_init.md`.
2. **Verificar consistencia cruzada:** comprobar alineación entre `DECISION_LOG.md`, `PROJECT_STATUS.yaml`, `CURRENT_STATE.md`, `DECISION_SPEC.md` y `TECHNICAL_CONTEXT.md`.
3. **Reportar diagnóstico y verificar autorización:** confirmar si existe autorización explícita del usuario o `ACTIVE_TASK.yaml` con `authorized: true`. Si no existe, detenerse.
4. **Confirmar alcance y rol activo:** delimitar entradas, salidas esperadas, criterios de aceptación y rol aplicable (`01_AGENT/roles/ROLES.md`).
5. **Consultar riesgos y supuestos:** revisar `00_GOVERNANCE/RISK_REGISTER.md`, `02_CONTEXT/ASSUMPTIONS.md` y `02_CONTEXT/OPEN_QUESTIONS.md`.
6. **Diseñar antes de construir:** asegurar que toda decisión de modelo, contrato de datos o arquitectura esté documentada antes de escribir código (`D01`–`D03` antes de `D04`).
7. **Ejecutar la tarea autorizada:** redactar entregables, implementar módulos o correr experimentos con `seed` explícita y validación *fail-fast*.
8. **Recolectar evidencia técnica:** documentar pruebas, métricas y rutas de resultados siguiendo `01_AGENT/protocols/evidence_collection.md`.
9. **Aplicar control de calidad:** validar el trabajo contra el checklist completo de `01_AGENT/protocols/quality_control.md` (incluyendo validación sintáctica de YAML/CSV y cero bloques anidados en Markdown).
10. **Actualizar memoria y estado:** sincronizar `PROJECT_STATUS.yaml`, `CURRENT_STATE.md`, `EXPERIMENT_LOG.csv`, `LESSONS.md` y `PROJECT_MEMORY.md` según `01_AGENT/protocols/memory_update.md` (sin alterar asientos históricos de `DECISION_LOG.md`).
11. **Entregar resumen verificable y solicitar aprobación:** reportar resultados, etiquetas epistemológicas, riesgos residuales y siguiente compuerta sugerida al responsable (`Sayd Quevedo`).

---

## 3. Qué Requiere Autorización Explícita

- Iniciar, modificar el alcance o cerrar como `approved` cualquier entregable (`D01`–`D06`).
- Agregar un nuevo asiento (`D-0002`, `D-0003`, ...) en `03_MEMORY/decisions/DECISION_LOG.md`.
- Seleccionar o cambiar el stack tecnológico (lenguaje, librerías de AG, formato de persistencia o framework de visualización).
- Modificar `00_GOVERNANCE/*`, `01_AGENT/prompts/active/prompt_activo.md` (cambio de versión SemVer) o `03_MEMORY/state/ACTIVE_TASK.yaml`.
- Crear o escribir archivos en `04_RESEARCH/D0X_*`, `05_DATA/`, `08_APPLICATION/`, `09_VALIDATION/`, `10_DOCUMENTATION/` o `11_OUTPUTS/`.

---

## 4. Qué NO Requiere Autorización Adicional

- Leer e inspeccionar cualquier archivo del repositorio durante Fase 0 o sesiones de auditoría en solo lectura.
- Emitir diagnósticos de consistencia, señalar contradicciones (`CONTRADICTED`), identificar riesgos nuevos o proponer planes de trabajo sin modificar archivos.
- Dentro de una tarea **ya autorizada** (`ACTIVE_TASK.yaml` con `authorized: true` y dentro de sus `constraints` explícitos): corregir erratas menores en los archivos del alcance asignado, ejecutar pruebas de solo validación sintáctica y completar los artefactos listados en `expected_outputs`.
