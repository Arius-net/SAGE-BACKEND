# Especificación `D02` — Arquitectura Modular y Matriz de Selección de Stack

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`
- **Resuelve:** `OQ-03` (`02_CONTEXT/OPEN_QUESTIONS.md`)
- **Asiento de aprobación:** `D-0002` (`03_MEMORY/decisions/DECISION_LOG.md`)

---

## 1. Matriz Comparativa de Alternativas Tecnológicas

Escala de evaluación: `1` (deficiente) a `5` (óptimo) según los criterios de `TECHNICAL_CONTEXT.md` (reproducibilidad por `seed`, transparencia académica del AG, soporte de gráficas, facilidad de pruebas *fail-fast* y cero dependencias de pago).

| Alternativa | Reproducibilidad (`seed`) | Transparencia del AG | Gráficas y tablas | Pruebas automatizadas | Costo / Portabilidad local | Puntaje total | Decisión |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Opción A: Python 3 + NumPy + Pandas + Matplotlib + PyYAML + pytest (AG modular propio)** | 5 | 5 | 5 | 5 | 5 | **25 / 25** | **SELECCIONADA** |
| **Opción B: Python 3 + DEAP / PyGAD** | 4 | 3 | 5 | 4 | 5 | 21 / 25 | Descartada (oculta detalles internos de cruce/mutación/diversidad Top-3 útiles para defensa en *Fundamentos de IA*) |
| **Opción C: Node.js / TypeScript + librería de gráficas externa** | 4 | 4 | 3 | 4 | 5 | 20 / 25 | Descartada (menor madurez para graficación científica reproducible local) |
| **Opción D: Java / C# + frameworks pesados** | 5 | 4 | 2 | 4 | 4 | 19 / 25 | Descartada (sobreingeniería y mayor fricción para iteración experimental) |

---

## 2. Stack Aprobado (`D-0002`)

| Capa | Tecnología seleccionada | Justificación técnica |
| :--- | :--- | :--- |
| Lenguaje | **Python 3.12+** | Disponible localmente, sintaxis clara para auditoría académica y determinismo exacto con `numpy.random.Generator` (`PCG64`). |
| Cálculo numérico y AG | **NumPy** (motor AG modular propio) | Vectorización rápida y control total sobre codificación del cromosoma, selección, cruce, mutación, elitismo y filtro de diversidad Top-3. |
| Tablas y análisis | **Pandas** | Exportación limpia de resultados tabulares (CSV/Markdown/JSON) y cálculo de comparativas Línea Base vs. Top-3. |
| Visualización | **Matplotlib** (backend `Agg` sin GUI) | Generación reproducible en local de gráficas PNG de alta resolución (convergencia del *Fitness*, nitrógeno, costo vs. producción y balance hídrico). |
| Configuración y catálogos | **JSON** (`05_DATA/reference/`) + **PyYAML** (`config/`, `03_MEMORY/state/`) | Legible por humanos, versionable en Git y validable en modo *fail-fast* sin motor de BD externo innecesario. |
| Pruebas y validación | **pytest** (`09_VALIDATION/`) | Suite clara de pruebas unitarias, integración, invariantes de dominio y determinismo por `seed`. |
| Interfaz de ejecución | **CLI estándar (`python -m sage.cli`)** | Reproducibilidad 100% automatizable sin sobreingeniería de servidor web. |

---

## 3. Arquitectura Modular (`08_APPLICATION/`)

    08_APPLICATION/
    └── sage/
        ├── __init__.py       # Versión y exportaciones públicas del paquete SAGE
        ├── models.py         # Estructuras tipadas: Crop, EnvParams, Parcel, EvaluationResult, RunResult
        ├── loader.py         # Cargador y validador fail-fast de crops_catalog, env_params y parcels_input
        ├── evaluator.py      # Simulador agronómico/económico y función Fitness (4 VO + penalizaciones)
        ├── baselines.py      # Generadores deterministas de Línea Base (monocultivo y rotación empírica)
        ├── ga_engine.py      # Motor del Algoritmo Genético (seed, selección, cruce, mutación, elitismo, Top-3)
        ├── reporting.py      # Exportación fail-fast de gráficas PNG, tablas CSV/JSON/Markdown y trazabilidad
        └── cli.py            # Punto de entrada CLI reproducible para corridas individuales y campañas D05

Flujo de datos unidireccional (sin mutación de entradas):

    05_DATA/reference/*.json -> loader (fail-fast) -> evaluator + baselines + ga_engine (seed) -> reporting (fail-fast) -> 11_OUTPUTS/
