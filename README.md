# SAGE — Sistema Agrícola de Genética Evolutiva

- **Versión:** `1.0.0`
- **Estado del proyecto:** Ciclo `D01`–`D06` **aprobado y cerrado** (`D-0005`, moneda `MXN`, `11/11` pruebas pasando)
- **Fecha de línea base:** `2026-11-23`
- **Autor / Responsable de aprobación:** Sayd Quevedo
- **Contexto:** Proyecto final académico — *Fundamentos de Inteligencia Artificial* (Ingeniería en TI e Innovación Digital)

---

## 1. Propósito

**SAGE (Sistema Agrícola de Genética Evolutiva)** es un Sistema de Apoyo a la Decisión (DSS) de naturaleza **prescriptiva y de optimización** basado en Algoritmos Genéticos (AG). Planifica de manera espaciotemporal la rotación de cultivos y la asignación de riego en unidades agrícolas de **3 a 10 parcelas** (piloto implementado: `5` parcelas, `18.0 ha`) durante **5 años (10 ciclos semestrales: Primavera-Verano `PV` y Otoño-Invierno `OI`)**, priorizando la regeneración de suelos (`N > 0`), la eficiencia hídrica y la maximización de utilidades.

SAGE **no es un sistema predictivo**: no pronostica clima ni precios de mercado; opera sobre catálogos agronómicos y parámetros de referencia estáticos (`05_DATA/reference/`) con datos sintéticos, sin PII, sin PHI y sin secretos reales.

---

## 2. Principio Rector

> **Decisión primero (DSS):** Cada dato, métrica, restricción y módulo existe únicamente para respaldar `DEC-01` y `DEC-02`. SAGE apoya la decisión con trazabilidad e incertidumbre explícita; nunca sustituye el criterio humano.

---

## 3. Stack Tecnológico Aprobado (`D-0002` / `D-0004`)

- **Lenguaje y motor evolutivo:** Python 3.12+ con **NumPy** (Algoritmo Genético modular propio y determinista `PCG64` en `BACKEND/sage/`).
- **Datos y salidas:** JSON (`05_DATA/reference/`), PyYAML (`config/`, `03_MEMORY/state/`), **Pandas** (tablas CSV/JSON/Markdown) y **Matplotlib** (`Agg`, gráficas PNG en `11_OUTPUTS/`).
- **Pruebas:** **pytest** (`09_VALIDATION/`, `11/11` pruebas pasando).

---

## 4. Guía de Ejecución Reproducible

Instalación de dependencias y ejecución de pruebas + campaña experimental `D05` en Windows PowerShell:

    pip install -r BACKEND/requirements.txt
    $env:PYTHONPATH="BACKEND"
    python -m pytest 09_VALIDATION -v
    python -m sage.cli campaign --data-dir 05_DATA/reference --output-dir 11_OUTPUTS --experiment-log 03_MEMORY/experiments/EXPERIMENT_LOG.csv

Ejecución de una corrida individual con semilla personalizada:

    $env:PYTHONPATH="BACKEND"
    python -m sage.cli run --seed 2026 --pop-size 140 --generations 180 --mutation-rate 0.05 --output-dir 11_OUTPUTS/custom_run

En Linux/macOS sustituye `$env:PYTHONPATH="BACKEND"` por `PYTHONPATH=BACKEND`.

---

## 5. Resumen de Resultados Verificados (`EXP-002`, `seed=2026`, `MXN`)

| Plan | Fitness | Costo Total (MXN) | Producción (ton) | Utilidad Neta (MXN) | N Final Prom (kg/ha) | Desvío Hídrico (mm) | Violaciones (`N/Temp/Mono`) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `Baseline_Monocultivo` | `-4.7114` | `3,204,000.00` | `328.32` | `-1,693,728.00` | `-268.00` | `75.00` | `45 / 25 / 45` |
| `Baseline_Rotacion_Empirica` | `0.5574` | `1,771,200.00` | `521.40` | `1,503,720.00` | `56.00` | `195.00` | `0 / 0 / 0` |
| **`SAGE_Top_1`** | **`0.7695`** | `2,045,775.00` | **`807.35`** | **`3,852,575.00`** | `73.60` | **`3.00`** | **`0 / 0 / 0`** |
| **`SAGE_Top_2`** | `0.7601` | `2,081,325.00` | `807.14` | `3,830,327.50` | `71.20` | `21.00` | **`0 / 0 / 0`** |
| **`SAGE_Top_3`** | `0.7593` | `2,084,325.00` | `798.92` | `3,804,250.00` | **`75.20`** | `27.00` | **`0 / 0 / 0`** |

---

## 6. Estructura del Repositorio

    ./
    ├── README.md
    ├── AGENTS.md
    ├── .env.example
    ├── .gitignore
    ├── BACKEND/
    │   ├── requirements.txt
    │   └── sage/            # Motor del Algoritmo Genético, evaluador, líneas base, reportes y CLI
    ├── config/environment.example.yaml
    ├── 00_GOVERNANCE/       # Acta constitutiva, DSS (DEC-01/02), reglas y riesgos
    ├── 01_AGENT/            # Protocolo Fase 0, roles, calidad y prompts SemVer
    ├── 02_CONTEXT/          # Contexto vigente, glosario, supuestos y preguntas abiertas
    ├── 03_MEMORY/           # DECISION_LOG inmutable, EXPERIMENT_LOG.csv, LESSONS y YAML de estado
    ├── 04_RESEARCH/         # Protocolo y entregables secuenciales D01..D06
    ├── 05_DATA/reference/   # Base de Conocimiento sintética (crops_catalog, env_params, parcels_input)
    ├── 09_VALIDATION/       # Suite pytest (11 pruebas unitarias e integración)
    ├── 10_DOCUMENTATION/    # Informe técnico final listo para defensa académica
    └── 11_OUTPUTS/          # Gráficas PNG y tablas CSV/JSON/Markdown de EXP-002 y experimentos

---

## 7. Puntos de Entrada Clave

- **Informe final para defensa académica:** `10_DOCUMENTATION/SAGE_FINAL_REPORT.md`
- **Reporte Top-3 y gráficas del mejor experimento:** `11_OUTPUTS/top3_report.md` y `11_OUTPUTS/*.png`
- **Decisiones de gobernanza (`D-0001`–`D-0005`):** `03_MEMORY/decisions/DECISION_LOG.md`
- **Código fuente del backend:** `BACKEND/sage/` y `BACKEND/requirements.txt`
- **Para agentes de IA:** iniciar siempre en `AGENTS.md` -> `01_AGENT/01_init.md` -> `01_AGENT/protocols/phase_0_inspection.md`
