# Verificación `D01` — Formulación del Problema y Línea Base

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`
- **Estado de verificación:** Aprobado para transición a `D02`

---

## 1. Matriz de Trazabilidad Epistemológica

| Elemento formulado | Fuente / Referencia | Etiqueta epistemológica |
| :--- | :--- | :--- |
| Naturaleza prescriptiva (no predictiva), 4 VD, 4 VO, `DEC-01`/`DEC-02` | `00_GOVERNANCE/PROJECT_CHARTER.md`, `03_MEMORY/decisions/DECISION_LOG.md` (`D-0001`) | `VERIFIED` |
| Escenario piloto `PILOT_5P_10C` (5 parcelas × 10 ciclos `PV`/`OI`) | `05_DATA/reference/parcels_input.json` | `SUPPORTED` |
| Coeficientes sintéticos de costos, precios, `ΔN` y demanda hídrica | `05_DATA/reference/crops_catalog.json`, `05_DATA/reference/env_params.json` | `ASSUMPTION` (registrado en `OPEN_QUESTIONS.md` para revisión final de Sayd Quevedo) |
| Pesos iniciales del Fitness (`0.38 / 0.22 / 0.22 / 0.18`) y penalizaciones | `05_DATA/reference/env_params.json` | `ASSUMPTION` (calibrado experimentalmente en `D05`) |

---

## 2. Cumplimiento de Criterios de `D01`

- [x] Se respetaron exactamente los 5 estados de cultivo (`0` Barbecho, `1` Maíz, `2` Frijol, `3` Sorgo, `4` Avena/Trigo) y las temporadas `PV`/`OI`.
- [x] Se incluyeron penalizaciones explícitas por monocultivo consecutivo, siembra fuera de ciclo `PV`/`OI` y agotamiento de nitrógeno (`N <= 0` / `N < 0`).
- [x] Se definieron dos líneas base deterministas comparables (`baseline_monoculture` y `baseline_empirical_rotation`).
- [x] Cero PII, cero PHI, cero secretos y `data_vintage = "2026-11-23"` explícito en todos los archivos de `05_DATA/reference/`.
