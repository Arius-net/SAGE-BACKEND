# Informe Técnico Final y Defensa Académica — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Materia:** *Fundamentos de Inteligencia Artificial* — Ingeniería en TI e Innovación Digital
- **Autor / Responsable de aprobación:** Sayd Quevedo
- **Versión:** `1.0.0` (Aprobada en `D-0005`)
- **Fecha de línea base:** `2026-11-23`
- **Frescura de datos (`data_vintage`):** `2026-11-23`
- **Moneda de referencia:** **MXN** (Pesos Mexicanos)

> **Aviso de Naturaleza DSS:** SAGE es un Sistema de Apoyo a la Decisión (DSS) estrictamente **prescriptivo / de optimización** basado en Algoritmos Genéticos sobre catálogos agronómicos estáticos. **No** predice clima ni precios y apoya al decisor sin sustituir el criterio humano.

---

## 1. Planteamiento del Problema

Planificar manualmente la rotación de cultivos y el riego de múltiples parcelas a lo largo de 5 años (`10` ciclos semestrales alternados **Primavera-Verano `PV`** y **Otoño-Invierno `OI`**) implica un espacio de búsqueda combinatorio de `25^50` configuraciones posibles en un predio piloto de `5` parcelas (`PILOT_5P_10C`, `18.0 ha` totales).

- **Variables de Decisión (VD — genes `(crop_id, irrigation_level)` por parcela y ciclo):**
  1. **Tipo de cultivo:** `0` = Barbecho/Descanso, `1` = Maíz, `2` = Frijol, `3` = Sorgo, `4` = Avena/Trigo.
  2. **Fecha:** ciclo semestral (`PV` / `OI`, ciclos `1..10`).
  3. **Riego:** nivel discreto `0..4` (`0, 150, 300, 450, 600 mm`).
  4. **Parcela:** `P1` a `P5` (áreas `2.5–5.0 ha`, `N_0` inicial `40–64 kg/ha`).
- **Variables a Optimizar (VO):**
  1. **Costo operativo total** (minimizar semillas, insumos, mantenimiento y agua en `MXN`).
  2. **Producción total** (maximizar toneladas y valor bruto cosechado en `MXN`).
  3. **Nivel de nutrientes del suelo** (maximizar y preservar nitrógeno estrictamente en `N > 0`).
  4. **Desperdicio de agua / estrés hídrico** (minimizar la desviación `|W_aplicado - W_requerido|`).
- **Decisiones apoyadas:**
  - `DEC-01` *(rebanada vertical)*: generación reproducible del calendario espaciotemporal `parcela × ciclo`.
  - `DEC-02` *(selección informada)*: comparación de los **3 mejores individuos estructuralmente distintos** evaluando *trade-offs* financieros, edáficos e hídricos.

---

## 2. Arquitectura y Stack Tecnológico (`D-0002` / `D-0004`)

Seleccionado mediante matriz comparativa en `04_RESEARCH/D02/01_SPEC.md` y consolidado en la carpeta raíz `BACKEND/` mediante `D-0004`:

- **Python 3.12 + NumPy:** motor evolutivo modular propio (`BACKEND/sage/`) con generador determinista `PCG64` (`seed` explícita), selección por torneo, cruce híbrido (por punto temporal por parcela y uniforme por gen), mutación cerrada en `{0..4} × {0..4}`, elitismo/poda y filtro de diversidad Top-3 basado en distancia de Hamming.
- **JSON + PyYAML:** Base de Conocimiento sintética en `05_DATA/reference/` (expresada en **MXN** según `D-0005`) validada en modo *fail-fast* (`DataValidationError`).
- **Pandas + Matplotlib (`Agg`):** exportación *fail-fast* (`ExportError`) de las 4 gráficas PNG obligatorias y reportes tabulares CSV/JSON/Markdown en `11_OUTPUTS/`.
- **pytest (`09_VALIDATION/`):** 11 pruebas automatizadas cubriendo esquemas, invariantes de operadores, determinismo por `seed`, líneas base y factibilidad `N > 0`.

---

## 3. Resultados Experimentales Verificados (`D05` / `D-0005` en MXN)

### 3.1 Calibración Multi-Experimento (`03_MEMORY/experiments/EXPERIMENT_LOG.csv`)

| Experimento | `seed` | Población / Gen | Cruce / Mutación | Fitness Top-1 | Utilidad Neta (MXN) | N Final Prom (kg/ha) | Desvío Hídrico (mm) | Estado |
| :--- | :---: | :---: | :---: | ---: | ---: | ---: | ---: | :--- |
| `EXP-001` | `42` | `80 / 140` | `0.85 / 0.08` | `0.7018` | `3,013,437.50` | `77.60` | `93.00` | Factible (`0/0/0`) |
| **`EXP-002`** | **`2026`** | **`140 / 180`** | **`0.88 / 0.05`** | **`0.7695`** | **`3,852,575.00`** | **`73.60`** | **`3.00`** | **Ganador (`0/0/0`)** |
| `EXP-003` | `777` | `100 / 160` | `0.80 / 0.14` | `0.6343` | `1,931,580.00` | `82.80` | `156.00` | Factible (`0/0/0`) |

### 3.2 Comparativa Final: Líneas Base vs. Top-3 de SAGE (`EXP-002`, MXN)

| Plan | Fitness | Costo Total (MXN) | Producción (ton) | Valor Bruto (MXN) | Utilidad Neta (MXN) | N Final Prom (kg/ha) | N Mín (kg/ha) | Desvío Hídrico (mm) | Violaciones (`N/Temp/Mono`) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `Baseline_Monocultivo` | `-4.7114` | `3,204,000.00` | `328.32` | `1,510,272.00` | `-1,693,728.00` | `-268.00` | `-280.00` | `75.00` | `45 / 25 / 45` |
| `Baseline_Rotacion_Empirica` | `0.5574` | `1,771,200.00` | `521.40` | `3,274,920.00` | `1,503,720.00` | `56.00` | `6.00` | `195.00` | `0 / 0 / 0` |
| **`SAGE_Top_1`** | **`0.7695`** | `2,045,775.00` | **`807.35`** | `5,898,350.00` | **`3,852,575.00`** | `73.60` | `36.00` | **`3.00`** | **`0 / 0 / 0`** |
| **`SAGE_Top_2`** | `0.7601` | `2,081,325.00` | `807.14` | **`5,911,652.50`** | `3,830,327.50` | `71.20` | `24.00` | `21.00` | **`0 / 0 / 0`** |
| **`SAGE_Top_3`** | `0.7593` | `2,084,325.00` | `798.92` | `5,888,575.00` | `3,804,250.00` | **`75.20`** | `36.00` | `27.00` | **`0 / 0 / 0`** |

### 3.3 Hallazgos Clave para Defensa Académica
1. **Valor del enfoque multiobjetivo frente al monocultivo:** el monocultivo continuo de Maíz colapsa el nitrógeno del suelo (`-268.00 kg/ha` al ciclo 10) y genera pérdidas netas de `-1,693,728.00 MXN`.
2. **Ventaja evolutiva frente a la heurística manual:** `SAGE_Top_1` incrementa el *Fitness* en **+38.1%**, eleva la utilidad neta en **+156.2%** (`+2,348,855.00 MXN` acumulados en 5 años), mejora el nitrógeno final promedio en **+31.4%** (`73.60` vs. `56.00 kg/ha`) y reduce la desviación hídrica en **-98.5%** (`3.00` vs. `195.00 mm`).
3. **Soporte real a `DEC-02`:** los tres mejores individuos tienen distancias de Hamming de `10`, `11` y `13` alelos y ofrecen perfiles claros (máxima utilidad y mínima desviación hídrica en Top-1, mayor valor bruto en Top-2, mayor regeneración edáfica en Top-3).

---

## 4. Guía de Ejecución Reproducible

Desde la raíz del repositorio en PowerShell (Windows):

    pip install -r BACKEND/requirements.txt
    $env:PYTHONPATH="BACKEND"
    python -m pytest 09_VALIDATION -v
    python -m sage.cli campaign --data-dir 05_DATA/reference --output-dir 11_OUTPUTS --experiment-log 03_MEMORY/experiments/EXPERIMENT_LOG.csv

Para ejecutar una corrida individual personalizada:

    $env:PYTHONPATH="BACKEND"
    python -m sage.cli run --seed 2026 --pop-size 140 --generations 180 --mutation-rate 0.05 --output-dir 11_OUTPUTS/custom_run

---

## 5. Artefactos Visuales y Tabulares (`11_OUTPUTS/`)

- `11_OUTPUTS/fitness_convergence.png` — Curva de convergencia (mejor, promedio, peor por generación + líneas base).
- `11_OUTPUTS/top3_nitrogen_evolution.png` — Evolución de nitrógeno `C0`–`C10` por parcela para los 3 mejores individuos.
- `11_OUTPUTS/top3_cost_vs_production.png` — Comparativa Costo, Producción y Utilidad Neta en **MXN** (Líneas Base vs. Top-3).
- `11_OUTPUTS/top3_water_balance.png` — Balance hídrico ciclo a ciclo (riego aplicado vs. requerido) del Top-3.
- `11_OUTPUTS/top3_summary.csv`, `11_OUTPUTS/top3_calendars.csv`, `11_OUTPUTS/top3_report.json`, `11_OUTPUTS/top3_report.md`.

---

## 6. Supuestos Aprobados y Limitaciones Explícitas

Todos los parámetros y supuestos (`ASM-01`–`ASM-05`, `OQ-01`–`OQ-08`) fueron revisados y aprobados formalmente por Sayd Quevedo en `D-0005`. Para aplicación productiva en campo real, la Base de Conocimiento sintética deberá calibrarse con análisis edáficos y tarifas locales vigentes.
