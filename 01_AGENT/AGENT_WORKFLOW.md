# Flujo de Trabajo Operativo del Agente — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`

---

## 1. Ciclo Operativo de 11 Pasos

Este flujo estandariza la ejecución de cualquier sesión de trabajo sobre SAGE, en total consistencia con `01_AGENT/AGENT_INSTRUCTIONS.md`:

1. **Inspección inicial (Fase 0):** ejecutar los 7 pasos de `01_AGENT/01_init.md` en modo solo lectura.
2. **Validación de coherencia:** aplicar `01_AGENT/protocols/phase_0_inspection.md` para confirmar consistencia de fechas, IDs (`D-0001`), decisiones (`DEC-01`/`DEC-02`), stack abierto y estado YAML.
3. **Compuerta de autorización:** verificar si existe autorización explícita del usuario o `03_MEMORY/state/ACTIVE_TASK.yaml` con `authorized: true`. Si no existe, emitir el diagnóstico de 4 puntos y detenerse.
4. **Encuadre de tarea y rol:** identificar el entregable activo (`D01`–`D06`), las entradas, las salidas esperadas y el rol principal según `01_AGENT/roles/ROLES.md`.
5. **Revisión de riesgos y supuestos:** consultar `RISK_REGISTER.md`, `ASSUMPTIONS.md` y `OPEN_QUESTIONS.md` para prevenir desviaciones.
6. **Diseño explícito antes de construir:** documentar especificación, contratos y criterios de prueba antes de codificar o correr experimentos.
7. **Ejecución controlada:** producir los artefactos del alcance autorizado aplicando *fail-fast*, reproducibilidad con `seed` (cuando aplique) y cero placeholders.
8. **Registro de evidencia técnica:** compilar resultados verificables conforme a `01_AGENT/protocols/evidence_collection.md`.
9. **Control de calidad:** ejecutar íntegramente `01_AGENT/protocols/quality_control.md`, verificando enlaces, consistencia, sintaxis YAML/CSV y ausencia de bloques de código anidados en Markdown.
10. **Sincronización de memoria y estado:** aplicar `01_AGENT/protocols/memory_update.md` manteniendo la inmutabilidad de `DECISION_LOG.md`.
11. **Cierre y reporte a aprobación:** presentar el resumen de verificación, el nivel epistemológico de los resultados y la propuesta del siguiente paso a **Sayd Quevedo**.

---

## 2. Contrato Obligatorio Antes de Escribir

Ningún agente transita del paso 3 al paso 4 (modo escritura) sin cumplir esta verificación binaria:

    [1] Fase 0 completada sin contradicciones críticas abiertas ........... OBLIGATORIO
    [2] Autorización explícita vigente (usuario o ACTIVE_TASK.yaml) ....... OBLIGATORIO
    [3] Alcance acotado a un objetivo concreto y sus constraints .......... OBLIGATORIO
    [4] Stack abierto respetado (si aún no se aprueba D02) ................ OBLIGATORIO
    [5] Cero PII, cero PHI, cero secretos en las salidas planeadas ........ OBLIGATORIO

Si cualquiera de las cinco condiciones es falsa, el agente debe permanecer en solo lectura y reportar el bloqueo exacto.
