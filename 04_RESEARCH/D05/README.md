# Entregable `D05` — Calibración, Experimentación Reproducible y Validación `DEC-02`

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Entregable:** `D05`
- **Versión:** `1.0.0`
- **Fecha:** `2026-11-23`
- **Experimento ganador:** `EXP-002` (`seed=2026`, `Fitness=0.7695`)

---

## Resumen Ejecutivo

Se ejecutó una campaña experimental reproducible de tres corridas calibradas (`EXP-001`, `EXP-002`, `EXP-003`) variando tamaño de población, generaciones, tasa de mutación y pesos de penalización, registrando todas las métricas en `03_MEMORY/experiments/EXPERIMENT_LOG.csv` y exportando todas las salidas obligatorias del mejor experimento (`EXP-002`) a `11_OUTPUTS/`.

---

## Artefactos Generados

- Documentación del entregable: `04_RESEARCH/D05/01_SPEC.md`, `04_RESEARCH/D05/02_VERIFICATION.md`.
- Registro oficial de experimentos: `03_MEMORY/experiments/EXPERIMENT_LOG.csv`.
- Salidas del mejor experimento (`EXP-002`) en `11_OUTPUTS/`:
  - `fitness_convergence.png`, `top3_nitrogen_evolution.png`, `top3_cost_vs_production.png`, `top3_water_balance.png`
  - `top3_summary.csv`, `top3_calendars.csv`, `top3_report.json`, `top3_report.md`, `campaign_summary.json`
- Salidas individuales de cada corrida en `11_OUTPUTS/experiments/EXP-001/`, `EXP-002/` y `EXP-003/`.
