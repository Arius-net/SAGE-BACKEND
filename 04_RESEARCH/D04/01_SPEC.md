# Especificación `D04` — Rebanada Vertical `DEC-01` Implementada

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`

---

## Módulos de `08_APPLICATION/sage/`

1. `models.py`: Estructuras inmutables (`Crop`, `Parcel`, `EnvParams`, `ScenarioData`, `GAConfig`, `GenerationStats`) y resultados (`EvaluationResult`, `GARunResult`).
2. `loader.py`: Validación estricta *fail-fast* (`DataValidationError`) de los 3 archivos JSON en `05_DATA/reference/`, coherencia de `data_vintage` e invariantes del cromosoma.
3. `evaluator.py`: Simulación exacta de 10 ciclos `PV`/`OI` para `P` parcelas calculando las 4 VO, trayectorias de nitrógeno, balance hídrico, penalizaciones explícitas (`V_nitrogen`, `V_season`, `V_mono`) e infactibilidad.
4. `baselines.py`: Generación y evaluación justa de `baseline_monoculture` y `baseline_empirical_rotation`.
5. `ga_engine.py`: Algoritmo Genético 100% determinista (`PCG64`), inicialización híbrida, torneo, cruce híbrido, mutación cerrada en `{0..4}`, elitismo/poda y selección de Top-3 con filtro de distancia de Hamming.
6. `reporting.py`: Exportación *fail-fast* (`ExportError`) de las 4 gráficas PNG obligatorias, tablas CSV, reporte JSON y reporte Markdown (`DEC-01` y `DEC-02`).
7. `cli.py`: Interfaz de línea de comandos (`run` y `campaign`) para ejecución reproducible sin dependencias externas.
