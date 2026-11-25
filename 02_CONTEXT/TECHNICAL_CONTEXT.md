# Contexto Técnico — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.2.0`
- **Fecha de línea base:** `2026-11-23`
- **Estado del stack tecnológico:** **Aprobado en `D02` (`D-0002`) y consolidado en `BACKEND/` (`D-0004`)**
- **Nivel epistemológico:** `VERIFIED`

---

## 1. Stack Tecnológico Aprobado (`D-0002` / `D-0004`)

De conformidad con la matriz comparativa documentada en `04_RESEARCH/D02/01_SPEC.md` y los asientos `D-0002` y `D-0004` en `03_MEMORY/decisions/DECISION_LOG.md`, el stack oficial de SAGE es:

| Componente | Tecnología aprobada | Propósito en SAGE |
| :--- | :--- | :--- |
| Lenguaje y runtime | **Python 3.12+** | Núcleo ejecutable local, portable y auditable sin dependencias de pago. |
| Motor evolutivo y cálculo numérico | **NumPy** (AG modular propio en `BACKEND/sage/`) | Representación matricial del cromosoma `(parcelas, ciclos, 2)`, operadores genéticos deterministas con `numpy.random.Generator` (`PCG64`) y filtro de diversidad Top-3. |
| Análisis y salidas tabulares | **Pandas** + JSON/CSV/Markdown | Exportación reproducible de métricas, comparativas Línea Base vs. Top-3 y calendarios `parcela × ciclo`. |
| Visualización científica | **Matplotlib** (backend `Agg`) | Generación de la gráfica de convergencia del *Fitness* y las gráficas de evolución de nitrógeno, Costo vs. Producción y balance hídrico en `11_OUTPUTS/`. |
| Catálogos y configuración | **JSON** (`05_DATA/reference/`) + **PyYAML** (`config/`, `03_MEMORY/state/`) | Almacenamiento versionado en Git con validación estricta *fail-fast*. |
| Pruebas y verificación | **pytest** (`09_VALIDATION/`) | Pruebas unitarias y de integración (`PYTHONPATH="BACKEND"`): esquemas, dominio de cruce/mutación, determinismo por `seed` y superación de línea base con `N > 0`. |
| Interfaz de ejecución | **CLI (`python -m sage.cli`)** | Ejecución local parametrizada sin sobreingeniería de servidores ni dependencias externas. |

---

## 2. Arquitectura de Carpetas Técnicas Activas

- `BACKEND/`: Código fuente centralizado (`BACKEND/sage/`: `models.py`, `loader.py`, `evaluator.py`, `baselines.py`, `ga_engine.py`, `reporting.py`, `cli.py`) y dependencias (`BACKEND/requirements.txt`). Reemplaza a `08_APPLICATION/` según `D-0004`.
- `05_DATA/reference/`: Base de Conocimiento sintética (`crops_catalog.json`, `env_params.json`, `parcels_input.json`) con `data_vintage = "2026-11-23"`.
- `09_VALIDATION/`: Suite `pytest` de pruebas unitarias y de integración apuntando a `BACKEND/`.
- `10_DOCUMENTATION/`: Documentación técnica y guía final de defensa académica.
- `11_OUTPUTS/`: Artefactos generados por corrida y por campaña experimental `D05` (gráficas PNG y reportes CSV/JSON/Markdown).

---

## 3. Restricciones Técnicas Permanentes

1. **Reproducibilidad exacta por `seed`:** Todo experimento o corrida recibe `--seed` explícita y produce exactamente los mismos resultados al repetirse.
2. **Validación *fail-fast*:** Errores de esquema, códigos fuera de `0..4`, parcelas fuera de `3..10`, `N0 <= 0` o fallos de exportación abortan explícitamente con excepción controlada (`DataValidationError` / `ExportError`).
3. **Cero secretos y cero dependencias de red en tiempo de corrida:** Ejecución 100% local con catálogos sintéticos estáticos.
4. **Trazabilidad visible en toda salida:** Todo gráfico y tabla incluye `seed`, `data_vintage`, `scenario_id` y nota de naturaleza prescriptiva estática.
