# Reporte Operativo Top-3 (`DEC-01` / `DEC-02`) — EXP-001

- **Escenario:** `PILOT_5P_10C` (5 parcelas × 10 ciclos `PV`/`OI`)
- **Semilla (`seed`):** `42`
- **Frescura de datos (`data_vintage`):** `2026-11-23`
- **Hiperparámetros:** población=`80`, generaciones=`140`, cruce=`0.85`, mutación=`0.08`, torneo=`4`, elitismo=`4`
- **Diversidad estructural Top-3 (distancia de Hamming en 100 alelos):** `Top1-Top2=13`, `Top1-Top3=12`, `Top2-Top3=18`

> AVISO PRESCRIPTIVO (DSS): SAGE optimiza rotación de cultivos y riego sobre catálogos estáticos de referencia (no pronostica clima ni precios). Apoya la decisión; no sustituye el criterio humano.

## 1. Tabla Comparativa: Líneas Base vs. Top-3 de SAGE

| Plan | Fitness | Costo Total (MXN) | Producción (ton) | Valor Bruto (MXN) | Utilidad Neta (MXN) | N Final Prom (kg/ha) | N Mín (kg/ha) | Desvío Hídrico Prom (mm) | Violaciones (N/Temp/Mono) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `Baseline_Monocultivo` | -3.5064 | 3,204,000.00 | 328.32 | 1,510,272.00 | -1,693,728.00 | -268.00 | -280.00 | 75.00 | 45/25/45 |
| `Baseline_Rotacion_Empirica` | 0.5574 | 1,771,200.00 | 521.40 | 3,274,920.00 | 1,503,720.00 | 56.00 | 6.00 | 195.00 | 0/0/0 |
| `SAGE_Top_1` | 0.7018 | 1,944,375.00 | 678.80 | 4,957,812.50 | 3,013,437.50 | 77.60 | 20.00 | 93.00 | 0/0/0 |
| `SAGE_Top_2` | 0.6971 | 1,879,575.00 | 672.01 | 4,738,277.50 | 2,858,702.50 | 73.20 | 38.00 | 90.00 | 0/0/0 |
| `SAGE_Top_3` | 0.6969 | 1,988,550.00 | 725.93 | 5,017,267.50 | 3,028,717.50 | 71.20 | 20.00 | 99.00 | 0/0/0 |

## 2. Calendarios Parcela × Ciclo de los 3 Mejores Individuos (`DEC-02`)

### Individuo `SAGE_Top_1` — Fitness `0.7018` | Utilidad Neta `3,013,437.50 MXN` | N Final Prom `77.60 kg/ha` | Desvío Hídrico `93.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Frij (450) | Barb (0) | Frij (300) | Av/Tr (300) | Maíz (600) | Frij (300) | Sorg (450) | Frij (300) | Sorg (450) | Frij (300) | 102.0 |
| P2 (3.5ha / 46) | Frij (450) | Av/Tr (450) | Maíz (600) | Barb (0) | Barb (300) | Frij (300) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 80.0 |
| P3 (5.0ha / 64) | Frij (300) | Barb (0) | Sorg (600) | Frij (150) | Maíz (0) | Av/Tr (600) | Frij (300) | Av/Tr (600) | Frij (450) | Av/Tr (600) | 80.0 |
| P4 (2.5ha / 40) | Barb (150) | Barb (150) | Barb (150) | Frij (150) | Maíz (450) | Av/Tr (450) | Frij (300) | Av/Tr (300) | Sorg (150) | Av/Tr (300) | 38.0 |
| P5 (3.0ha / 52) | Frij (300) | Barb (0) | Maíz (600) | Frij (300) | Barb (0) | Frij (150) | Sorg (450) | Av/Tr (300) | Frij (150) | Av/Tr (450) | 88.0 |

### Individuo `SAGE_Top_2` — Fitness `0.6971` | Utilidad Neta `2,858,702.50 MXN` | N Final Prom `73.20 kg/ha` | Desvío Hídrico `90.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Sorg (600) | Barb (0) | Frij (300) | Av/Tr (300) | Maíz (600) | Frij (300) | Sorg (450) | Frij (600) | Sorg (300) | Frij (300) | 70.0 |
| P2 (3.5ha / 46) | Frij (450) | Av/Tr (450) | Frij (600) | Barb (0) | Barb (0) | Frij (300) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 104.0 |
| P3 (5.0ha / 64) | Frij (450) | Barb (0) | Sorg (600) | Frij (150) | Barb (0) | Av/Tr (600) | Frij (300) | Av/Tr (600) | Sorg (600) | Av/Tr (600) | 64.0 |
| P4 (2.5ha / 40) | Frij (150) | Barb (150) | Barb (150) | Frij (150) | Maíz (450) | Av/Tr (450) | Frij (300) | Av/Tr (300) | Sorg (150) | Av/Tr (300) | 38.0 |
| P5 (3.0ha / 52) | Frij (300) | Barb (0) | Maíz (600) | Frij (300) | Barb (0) | Frij (150) | Sorg (450) | Av/Tr (300) | Barb (150) | Av/Tr (300) | 90.0 |

### Individuo `SAGE_Top_3` — Fitness `0.6969` | Utilidad Neta `3,028,717.50 MXN` | N Final Prom `71.20 kg/ha` | Desvío Hídrico `99.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Barb (600) | Barb (0) | Frij (300) | Av/Tr (300) | Maíz (600) | Frij (300) | Sorg (450) | Frij (300) | Sorg (450) | Frij (300) | 102.0 |
| P2 (3.5ha / 46) | Frij (450) | Av/Tr (600) | Maíz (600) | Barb (0) | Barb (300) | Frij (300) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 80.0 |
| P3 (5.0ha / 64) | Frij (300) | Barb (0) | Maíz (600) | Frij (150) | Maíz (600) | Av/Tr (600) | Frij (300) | Av/Tr (600) | Frij (450) | Av/Tr (600) | 68.0 |
| P4 (2.5ha / 40) | Frij (150) | Barb (150) | Barb (150) | Frij (150) | Maíz (450) | Av/Tr (450) | Frij (300) | Av/Tr (600) | Sorg (150) | Av/Tr (300) | 38.0 |
| P5 (3.0ha / 52) | Sorg (450) | Barb (0) | Maíz (600) | Frij (300) | Barb (0) | Frij (150) | Sorg (300) | Av/Tr (300) | Frij (0) | Av/Tr (300) | 68.0 |
