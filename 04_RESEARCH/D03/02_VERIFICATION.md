# Verificación `D03` — Contratos de Datos, Cromosoma y Operadores

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`
- **Estado:** Verificado y mapeado a pruebas automatizadas en `09_VALIDATION/`

---

## Trazabilidad Diseño -> Pruebas (`09_VALIDATION/`)

| Invariante diseñado en `D03` | Riesgo mitigado | Prueba en `09_VALIDATION/` |
| :--- | :--- | :--- |
| Validación *fail-fast* de `crops_catalog`, `env_params` y `parcels_input` | `RSK-04`, `RSK-06` | `test_loader.py` |
| Dominio cerrado de genes `{0..4} × {0..4}` tras cruce y mutación | `RSK-03` | `test_ga_operators.py` |
| Reproducibilidad bit a bit dada la misma `seed` | `RSK-06` | `test_ga_integration.py` |
| Separación estricta de infactibilidad `N <= 0` y superación de línea base | `RSK-02` | `test_evaluator_and_baselines.py`, `test_ga_integration.py` |
| Unicidad y diversidad estructural del Top-3 (`DEC-02`) | `RSK-01` | `test_ga_integration.py` |
