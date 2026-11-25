# Entregable `D03` — Diseño de Datos, Modelo de Cromosoma y Operadores Genéticos

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Entregable:** `D03`
- **Versión:** `1.0.0`
- **Fecha:** `2026-11-23`
- **Dependencias:** `D01` (formulación y línea base) y `D02` (stack aprobado en `D-0002`)

---

## Resumen Ejecutivo

Este entregable especifica los contratos exactos de validación *fail-fast* de datos (`crops_catalog.json`, `env_params.json`, `parcels_input.json`), la codificación matricial del cromosoma `[parcelas × ciclos × 2]` con genes `(crop_id, irrigation_level)`, los operadores evolutivos (inicialización con `seed`, selección por torneo, cruce, mutación con garantía de dominio, elitismo/poda) y el algoritmo de selección de los **3 mejores individuos estructuralmente distintos** para `DEC-02`.

---

## Contenido del Entregable

- `04_RESEARCH/D03/01_SPEC.md`: Esquemas de datos, invariantes *fail-fast*, codificación del cromosoma, operadores genéticos y criterio de diversidad Top-3.
- `04_RESEARCH/D03/02_VERIFICATION.md`: Matriz de invariantes y trazabilidad hacia los casos de prueba de `09_VALIDATION/`.
