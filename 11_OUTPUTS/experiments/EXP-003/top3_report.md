# Reporte Operativo Top-3 (`DEC-01` / `DEC-02`) — EXP-003

- **Escenario:** `PILOT_5P_10C` (5 parcelas × 10 ciclos `PV`/`OI`)
- **Semilla (`seed`):** `777`
- **Frescura de datos (`data_vintage`):** `2026-11-23`
- **Hiperparámetros:** población=`100`, generaciones=`160`, cruce=`0.8`, mutación=`0.14`, torneo=`3`, elitismo=`4`
- **Diversidad estructural Top-3 (distancia de Hamming en 100 alelos):** `Top1-Top2=41`, `Top1-Top3=20`, `Top2-Top3=27`

> AVISO PRESCRIPTIVO (DSS): SAGE optimiza rotación de cultivos y riego sobre catálogos estáticos de referencia (no pronostica clima ni precios). Apoya la decisión; no sustituye el criterio humano.

## 1. Tabla Comparativa: Líneas Base vs. Top-3 de SAGE

| Plan | Fitness | Costo Total (MXN) | Producción (ton) | Valor Bruto (MXN) | Utilidad Neta (MXN) | N Final Prom (kg/ha) | N Mín (kg/ha) | Desvío Hídrico Prom (mm) | Violaciones (N/Temp/Mono) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `Baseline_Monocultivo` | -2.8464 | 3,204,000.00 | 328.32 | 1,510,272.00 | -1,693,728.00 | -268.00 | -280.00 | 75.00 | 45/25/45 |
| `Baseline_Rotacion_Empirica` | 0.5574 | 1,771,200.00 | 521.40 | 3,274,920.00 | 1,503,720.00 | 56.00 | 6.00 | 195.00 | 0/0/0 |
| `SAGE_Top_1` | 0.6343 | 1,697,150.00 | 557.72 | 3,628,730.00 | 1,931,580.00 | 82.80 | 26.00 | 156.00 | 0/0/0 |
| `SAGE_Top_2` | 0.6287 | 1,777,650.00 | 569.13 | 3,756,547.50 | 1,978,897.50 | 64.40 | 32.00 | 180.00 | 0/0/0 |
| `SAGE_Top_3` | 0.6276 | 1,728,075.00 | 556.62 | 3,694,630.00 | 1,966,555.00 | 79.60 | 26.00 | 153.00 | 0/0/1 |

## 2. Calendarios Parcela × Ciclo de los 3 Mejores Individuos (`DEC-02`)

### Individuo `SAGE_Top_1` — Fitness `0.6343` | Utilidad Neta `1,931,580.00 MXN` | N Final Prom `82.80 kg/ha` | Desvío Hídrico `156.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Maíz (450) | Frij (450) | Barb (150) | Barb (150) | Frij (300) | Barb (600) | Maíz (450) | Barb (300) | Frij (300) | Av/Tr (300) | 102.0 |
| P2 (3.5ha / 46) | Frij (600) | Av/Tr (300) | Barb (450) | Barb (300) | Maíz (450) | Barb (600) | Barb (150) | Barb (300) | Sorg (300) | Frij (300) | 120.0 |
| P3 (5.0ha / 64) | Barb (0) | Av/Tr (600) | Barb (150) | Av/Tr (450) | Sorg (450) | Frij (150) | Maíz (600) | Frij (150) | Maíz (450) | Av/Tr (300) | 26.0 |
| P4 (2.5ha / 40) | Barb (450) | Frij (150) | Barb (300) | Frij (0) | Barb (0) | Av/Tr (300) | Maíz (450) | Barb (600) | Maíz (300) | Frij (300) | 88.0 |
| P5 (3.0ha / 52) | Barb (0) | Frij (150) | Barb (0) | Av/Tr (300) | Sorg (600) | Av/Tr (300) | Frij (150) | Av/Tr (150) | Barb (0) | Av/Tr (450) | 78.0 |

### Individuo `SAGE_Top_2` — Fitness `0.6287` | Utilidad Neta `1,978,897.50 MXN` | N Final Prom `64.40 kg/ha` | Desvío Hídrico `180.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Sorg (450) | Frij (600) | Barb (0) | Barb (150) | Frij (150) | Barb (600) | Maíz (600) | Frij (600) | Maíz (450) | Av/Tr (450) | 62.0 |
| P2 (3.5ha / 46) | Frij (600) | Av/Tr (300) | Barb (300) | Frij (450) | Maíz (450) | Av/Tr (600) | Sorg (600) | Barb (300) | Sorg (300) | Frij (300) | 62.0 |
| P3 (5.0ha / 64) | Barb (0) | Barb (300) | Barb (150) | Av/Tr (450) | Sorg (450) | Frij (0) | Maíz (600) | Frij (450) | Maíz (450) | Av/Tr (300) | 48.0 |
| P4 (2.5ha / 40) | Frij (300) | Av/Tr (0) | Barb (150) | Av/Tr (150) | Frij (600) | Av/Tr (300) | Sorg (0) | Frij (600) | Sorg (0) | Frij (300) | 68.0 |
| P5 (3.0ha / 52) | Barb (0) | Frij (150) | Barb (0) | Barb (0) | Frij (0) | Av/Tr (300) | Frij (450) | Barb (150) | Sorg (0) | Av/Tr (450) | 82.0 |

### Individuo `SAGE_Top_3` — Fitness `0.6276` | Utilidad Neta `1,966,555.00 MXN` | N Final Prom `79.60 kg/ha` | Desvío Hídrico `153.00 mm`

| Parcela (Área / N0) | C1 (PV) | C2 (OI) | C3 (PV) | C4 (OI) | C5 (PV) | C6 (OI) | C7 (PV) | C8 (OI) | C9 (PV) | C10 (OI) | N Final |
| :--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| P1 (4.0ha / 58) | Sorg (450) | Frij (0) | Barb (150) | Av/Tr (150) | Frij (300) | Barb (600) | Maíz (600) | Barb (600) | Maíz (450) | Av/Tr (450) | 64.0 |
| P2 (3.5ha / 46) | Frij (600) | Barb (300) | Barb (150) | Frij (300) | Maíz (450) | Barb (600) | Barb (600) | Barb (300) | Sorg (300) | Frij (300) | 120.0 |
| P3 (5.0ha / 64) | Barb (0) | Av/Tr (300) | Barb (150) | Av/Tr (450) | Sorg (450) | Frij (150) | Maíz (600) | Frij (150) | Maíz (450) | Av/Tr (300) | 26.0 |
| P4 (2.5ha / 40) | Frij (450) | Frij (150) | Barb (300) | Frij (0) | Barb (0) | Av/Tr (300) | Maíz (450) | Frij (600) | Maíz (300) | Frij (300) | 86.0 |
| P5 (3.0ha / 52) | Barb (0) | Frij (150) | Barb (0) | Barb (0) | Frij (0) | Av/Tr (300) | Frij (450) | Av/Tr (150) | Barb (0) | Av/Tr (450) | 102.0 |
