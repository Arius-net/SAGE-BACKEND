# Verificación `D04` — Suite de Pruebas de Rebanada Vertical `DEC-01`

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`

---

## Cobertura de Pruebas (`09_VALIDATION/`)

- `test_loader.py`: Verifica carga válida de `PILOT_5P_10C` y rechazo *fail-fast* ante falta de `crop_id`, `N0 <= 0`, pesos que no suman `1.0`, inconsistencia de `data_vintage` y alelos fuera de `{0..4}`.
- `test_evaluator_and_baselines.py`: Verifica que el monocultivo continuo agota el suelo (`N <= 0`) y recibe penalizaciones, mientras la rotación empírica permanece factible pero con desviación hídrica subóptima.
- `test_ga_operators.py`: Ejecuta 200 ciclos de cruce y mutación agresiva validando cierre estricto del dominio `{0..4} × {0..4}`.
- `test_ga_integration.py`: Comprueba determinismo exacto ante la misma `seed`, superación de ambas líneas base, cumplimiento de `N > 0` en el 100% de parcelas en todos los ciclos, diversidad estructural del Top-3 y generación íntegra de los 8 archivos obligatorios.
