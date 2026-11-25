# Especificación y Resultados `D05` — Calibración y Validación `DEC-02`

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`
- **Nivel epistemológico:** `VERIFIED` (corridas reproducibles ejecutadas y registradas en `EXPERIMENT_LOG.csv`)

---

## 1. Diseño y Resultados de la Campaña Experimental (`EXP-001`–`EXP-003`)

| Experimento | `seed` | Población / Gen | Cruce / Mutación | Penalizaciones | Fitness Top-1 | Utilidad Neta (USD) | N Final Prom (kg/ha) | Desvío Hídrico (mm) | Factible (`N > 0`) |
| :--- | :---: | :---: | :---: | :--- | ---: | ---: | ---: | ---: | :---: |
| `EXP-001` | `42` | `80 / 140` | `0.85 / 0.08` | Base (`2.50 / 0.85 / 0.65`) | `0.7018` | `150,671.88` | `77.60` | `93.00` | Sí (`0/0/0`) |
| **`EXP-002`** | **`2026`** | **`140 / 180`** | **`0.88 / 0.05`** | **Estricta (`3.50 / 1.10 / 0.85`)** | **`0.7695`** | **`192,628.75`** | **`73.60`** | **`3.00`** | **Sí (`0/0/0`)** |
| `EXP-003` | `777` | `100 / 160` | `0.80 / 0.14` | Moderada (`2.00 / 0.70 / 0.50`) | `0.6343` | `96,579.00` | `82.80` | `156.00` | Sí (`0/0/0`) |

### Análisis de Sensibilidad Observado
1. **Efecto de mutación excesiva (`EXP-003`, `mut=0.14`):** aunque mantiene factibilidad edáfica (`N > 0`), perturba excesivamente los bloques de riego óptimos, elevando el desvío hídrico a `156.00 mm` y reduciendo la utilidad neta a `96,579.00 USD`.
2. **Equilibrio exploración/explotación (`EXP-002`, `pop=140, gen=180, mut=0.05`):** permite sincronizar cultivo, temporada y nivel exacto de riego por parcela, reduciendo el desvío hídrico promedio a apenas **`3.00 mm`** (solo 1 de 50 genes fuera del requerimiento exacto) y alcanzando **`192,628.75 USD`** de utilidad neta con `0` violaciones.

---

## 2. Validación de `DEC-02` — Comparativa Líneas Base vs. Top-3 (`EXP-002`)

| Plan | Fitness | Costo (USD) | Producción (ton) | Valor Bruto (USD) | Utilidad Neta (USD) | N Final Prom (kg/ha) | N Mín (kg/ha) | Desvío Hídrico (mm) | Violaciones |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `Baseline_Monocultivo` | `-4.7114` | `160,200.00` | `328.32` | `75,513.60` | `-84,686.40` | `-268.00` | `-280.00` | `75.00` | `45/25/45` |
| `Baseline_Rotacion_Empirica` | `0.5574` | `88,560.00` | `521.40` | `163,746.00` | `75,186.00` | `56.00` | `6.00` | `195.00` | `0/0/0` |
| `SAGE_Top_1` | `0.7695` | `102,288.75` | `807.35` | `294,917.50` | `192,628.75` | `73.60` | `36.00` | `3.00` | `0/0/0` |
| `SAGE_Top_2` | `0.7601` | `104,066.25` | `807.14` | `295,582.62` | `191,516.38` | `71.20` | `24.00` | `21.00` | `0/0/0` |
| `SAGE_Top_3` | `0.7593` | `104,216.25` | `798.92` | `294,428.75` | `190,212.50` | `75.20` | `36.00` | `27.00` | `0/0/0` |

### *Trade-offs* del Top-3 para el Decisor Humano (`DEC-02`)
- **Distancia estructural verificada (sobre 100 alelos):** `Top1-Top2 = 10`, `Top1-Top3 = 11`, `Top2-Top3 = 13`.
- **`SAGE_Top_1`:** mejor balance integral (`Fitness 0.7695`), mayor utilidad neta (`192,628.75 USD`) y mínima desviación hídrica (`3.00 mm`).
- **`SAGE_Top_2`:** máximo valor bruto cosechado (`295,582.62 USD`), con mayor costo operativo y margen de nitrógeno ligeramente más ajustado (`N mín = 24.00 kg/ha`).
- **`SAGE_Top_3`:** mayor regeneración edáfica al cierre (`75.20 kg/ha` promedio; `P5` alcanza `102.0 kg/ha`), ideal para un perfil conservador en salud del suelo.
