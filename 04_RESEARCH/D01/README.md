# Entregable `D01` — Formulación del Problema y Línea Base

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Entregable:** `D01`
- **Versión:** `1.0.0`
- **Fecha:** `2026-11-23`
- **Estado:** Completado (`VERIFIED` tras ejecución de línea base en `D04`)
- **Autorización:** Autorización autónoma end-to-end otorgada por Sayd Quevedo (base `D-0001`)

---

## Resumen Ejecutivo

Este entregable formaliza matemáticamente el problema prescriptivo de optimización espaciotemporal de rotación de cultivos y riego para SAGE (`DEC-01` y `DEC-02`), define el escenario piloto sintético `PILOT_5P_10C` (`5` parcelas × `10` ciclos `PV`/`OI`) en `05_DATA/reference/` y establece dos líneas base explícitas (monocultivo y rotación empírica manual con riego fijo) para evaluar el valor agregado real del Algoritmo Genético.

---

## Contenido del Entregable

- `04_RESEARCH/D01/01_SPEC.md`: Formulación matemática completa de las 4 VD, las 4 VO, la función *Fitness* normalizada, las penalizaciones explícitas y las reglas de la línea base.
- `04_RESEARCH/D01/02_VERIFICATION.md`: Trazabilidad epistemológica, supuestos aplicados (`ASM-01`–`ASM-05`) y verificación frente a `PROJECT_CHARTER.md` y `DECISION_SPEC.md`.
- Datos sintéticos de referencia creados en `05_DATA/reference/`:
  - `05_DATA/reference/crops_catalog.json`
  - `05_DATA/reference/env_params.json`
  - `05_DATA/reference/parcels_input.json`
