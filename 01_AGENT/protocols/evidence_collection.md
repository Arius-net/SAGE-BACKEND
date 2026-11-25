# Protocolo de Recolección de Evidencia Técnica — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Modalidad de evidencia:** **Técnica únicamente** (sin encuestas ni trabajo de campo; no existe ni debe crearse registro de evidencia de campo)

---

## 1. Principio de Evidencia Técnica

En SAGE ninguna afirmación de desempeño, mejora frente a la línea base o validez del Algoritmo Genético se acepta sin evidencia técnica reproducible. Toda pieza de evidencia debe poder regenerarse de manera determinista a partir del repositorio y clasificarse con su etiqueta epistemológica (`VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN`, `CONTRADICTED`).

---

## 2. Tipos de Evidencia Obligatoria

| Tipo de evidencia | Ubicación prevista | Requisitos mínimos de validez |
| :--- | :--- | :--- |
| **Corridas reproducibles del AG (`seed`)** | `11_OUTPUTS/<run_id>/` | Metadatos completos: `run_id`, `seed`, `data_vintage`, versiones de `crops_catalog`, `env_params`, `parcels_input` y `code_version`. |
| **Bitácora estructurada de experimentos** | `03_MEMORY/experiments/EXPERIMENT_LOG.csv` | Fila anexada con las 12 columnas completas (`experiment_id`, `date`, `objective`, `dataset_version`, `code_version`, `method`, `parameters`, `validation_method`, `metrics`, `result_path`, `status`, `limitations`). |
| **Pruebas unitarias y de invariantes** | `09_VALIDATION/` | Cobertura verificable de carga *fail-fast*, dominio de cultivos (`0..4`), restricción `N > 0`, balance hídrico, diversidad Top-3 y reproducibilidad exacta con igual `seed`. |
| **Gráfica de convergencia del *Fitness*** | `11_OUTPUTS/<run_id>/` | Serie completa por generación de **mejor**, **promedio** y **peor** *Fitness*, con `seed` y `data_vintage` visibles. |
| **Reportes tabulares y visuales del Top-3** | `11_OUTPUTS/<run_id>/` | Exposición íntegra de los **3 mejores individuos distintos**: calendario parcela × ciclo (10 ciclos `PV`/`OI`), evolución de nitrógeno (`N`), balance costo/producción, balance hídrico y contraste con la línea base. |

---

## 3. Reglas de Registro y Verificación

1. **Prohibido fabricar o extrapolar métricas:** cada valor numérico en entregables `D04`–`D06` debe apuntar a un `experiment_id` real en `EXPERIMENT_LOG.csv` y a su ruta exacta en `11_OUTPUTS/`.
2. **Limitaciones obligatorias:** toda fila registrada en `EXPERIMENT_LOG.csv` debe declarar explícitamente sus limitaciones (por ejemplo, parámetros estáticos `ASM-01`, balance simplificado de nitrógeno `ASM-02` o sensibilidad de pesos).
3. **Corridas fallidas también se documentan:** si una calibración diverge, viola `N > 0` o sufre convergencia prematura (`RSK-01`), se registra con `status` fallido o descartado para preservar trazabilidad científica y extraer lecciones en `03_MEMORY/lessons_learned/LESSONS.md`.
4. **Comprobación de determinismo:** antes de marcar como `VERIFIED` cualquier resultado principal de `D04` o `D05`, repetir la ejecución con la misma `seed` y comprobar igualdad exacta de métricas.
