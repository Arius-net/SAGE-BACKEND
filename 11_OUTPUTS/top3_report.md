# Reporte Operativo Top-3 (`DEC-01` / `DEC-02`) — EXP-002

- **Escenario:** `PILOT_5P_10C` (5 parcelas × 10 ciclos `PV`/`OI`)
- **Semilla (`seed`):** `2026`
- **Frescura de datos (`data_vintage`):** `2026-11-23`
- **Hiperparámetros:** población=`140`, generaciones=`180`, cruce=`0.88`, mutación=`0.05`, torneo=`5`, elitismo=`6`
- **Diversidad estructural Top-3 (distancia de Hamming en 100 alelos):** `Top1-Top2=10`, `Top1-Top3=11`, `Top2-Top3=13`

> AVISO PRESCRIPTIVO (DSS): SAGE optimiza rotación de cultivos y riego sobre catálogos estáticos de referencia (no pronostica clima ni precios). Apoya la decisión; no sustituye el criterio humano.

## 1. Tabla Comparativa: Líneas Base vs. Top-3 de SAGE

| Plan | Fitness | Costo Total (MXN) | Producción (ton) | Valor Bruto (MXN) | Utilidad Neta (MXN) | N Final Prom (kg/ha) | N Mín (kg/ha) | Desvío Hídrico Prom (mm) | Violaciones (N/Temp/Mono) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `Baseline_Monocultivo` | -4.7114 | 3,204,000.00 | 328.32 | 1,510,272.00 | -1,693,728.00 | -268.00 | -280.00 | 75.00 | 45/25/45 |
| `Baseline_Rotacion_Empirica` | 0.5574 | 1,771,200.00 | 521.40 | 3,274,920.00 | 1,503,720.00 | 56.00 | 6.00 | 195.00 | 0/0/0 |
| `SAGE_Top_1` | 0.7695 | 2,045,775.00 | 807.35 | 5,898,350.00 | 3,852,575.00 | 73.60 | 36.00 | 3.00 | 0/0/0 |
| `SAGE_Top_2` | 0.7601 | 2,081,325.00 | 807.14 | 5,911,652.50 | 3,830,327.50 | 71.20 | 24.00 | 21.00 | 0/0/0 |
| `SAGE_Top_3` | 0.7593 | 2,084,325.00 | 798.92 | 5,888,575.00 | 3,804,250.00 | 75.20 | 36.00 | 27.00 | 0/0/0 |

## 2. Calendarios Parcela × Ciclo de los 3 Mejores Individuos (`DEC-02`)

### Individuo `SAGE_Top_1` — Fitness `0.7695` | Utilidad Neta `3,852,575.00 MXN` | N Final Prom `73.60 kg/ha` | Desvío Hídrico `3.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Frij (300) | Barb (0) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 76.0 |
| P2 (3.5ha / 46) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Sorg (450) | Frij (150) | Maíz (600) | Frij (150) | 60.0 |
| P3 (5.0ha / 64) | Barb (0) | Frij (150) | Sorg (450) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Maíz (600) | Frij (150) | 80.0 |
| P4 (2.5ha / 40) | Barb (150) | Frij (150) | Sorg (450) | Frij (150) | Sorg (450) | Frij (150) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 82.0 |
| P5 (3.0ha / 52) | Frij (300) | Av/Tr (300) | Frij (300) | Barb (0) | Maíz (600) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | 70.0 |

### Individuo `SAGE_Top_2` — Fitness `0.7601` | Utilidad Neta `3,830,327.50 MXN` | N Final Prom `71.20 kg/ha` | Desvío Hídrico `21.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Frij (450) | Barb (0) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 76.0 |
| P2 (3.5ha / 46) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Maíz (450) | Frij (150) | Maíz (600) | Frij (150) | 48.0 |
| P3 (5.0ha / 64) | Barb (0) | Frij (150) | Sorg (450) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Frij (450) | Av/Tr (300) | Maíz (600) | Frij (150) | 80.0 |
| P4 (2.5ha / 40) | Barb (150) | Frij (150) | Maíz (600) | Frij (150) | Sorg (450) | Frij (300) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 70.0 |
| P5 (3.0ha / 52) | Frij (300) | Av/Tr (450) | Frij (300) | Barb (0) | Sorg (450) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (450) | 82.0 |

### Individuo `SAGE_Top_3` — Fitness `0.7593` | Utilidad Neta `3,804,250.00 MXN` | N Final Prom `75.20 kg/ha` | Desvío Hídrico `27.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Frij (450) | Barb (0) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | Maíz (600) | Frij (150) | 76.0 |
| P2 (3.5ha / 46) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Sorg (450) | Frij (150) | Maíz (600) | Frij (150) | 60.0 |
| P3 (5.0ha / 64) | Barb (0) | Frij (150) | Maíz (450) | Av/Tr (300) | Frij (600) | Av/Tr (300) | Frij (300) | Av/Tr (300) | Maíz (600) | Frij (150) | 68.0 |
| P4 (2.5ha / 40) | Barb (150) | Frij (150) | Maíz (600) | Frij (150) | Sorg (450) | Frij (150) | Maíz (600) | Frij (300) | Maíz (600) | Frij (150) | 70.0 |
| P5 (3.0ha / 52) | Frij (300) | Av/Tr (300) | Frij (300) | Barb (0) | Maíz (600) | Frij (300) | Barb (0) | Av/Tr (450) | Frij (300) | Av/Tr (450) | 102.0 |
