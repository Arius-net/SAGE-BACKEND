# Registro de Riesgos — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Autor / Responsable de aprobación:** Sayd Quevedo

---

## Matriz de Riesgos Identificados

| ID | Riesgo | Impacto | Probabilidad | Mitigación |
| :--- | :--- | :--- | :--- | :--- |
| `RSK-01` | **Convergencia prematura en óptimos locales:** la población pierde diversidad genética en pocas generaciones y entrega 3 individuos casi idénticos o subóptimos. | Alto | Media | Incorporar control de diversidad poblacional, tasas de mutación calibradas, elitismo acotado, filtro de unicidad estructural para el Top-3 (`DEC-02`) y análisis sistemático de la curva de convergencia (mejor, promedio, peor) en `D05`. |
| `RSK-02` | **Mal calibrado de pesos y penalizaciones en la función Fitness:** un objetivo domina indebidamente a los demás (por ejemplo, maximizar producción destruyendo el nitrógeno del suelo o disparando el consumo de agua). | Crítico | Alta | Diseñar normalización explícita de las 4 VO y penalizaciones severas ante `N <= 0` en `D03`; realizar pruebas de sensibilidad y comparación directa contra la línea base en `D05` antes de aprobar el modelo. |
| `RSK-03` | **Violación de restricciones agronómicas o de dominio por cruce/mutación:** los operadores genéticos producen cultivos fuera del catálogo `0..4`, riegos negativos o combinaciones inválidas para el ciclo `PV`/`OI`. | Alto | Media | Definir operadores conscientes del dominio o mecanismos deterministas de reparación/validación en `D03`, respaldados por pruebas unitarias de invariantes en `D04`. |
| `RSK-04` | **Fallo parcial al generar o exportar salidas obligatorias:** el motor termina el AG pero falla la generación de la gráfica de convergencia o de alguna vista tabular/visual de los 3 mejores individuos, dejando entregables incompletos. | Medio | Media | Aplicar política estricta *fail-fast* en el pipeline de exportación (`DATA_CONTEXT.md`), validar la existencia e integridad de todas las salidas obligatorias antes de marcar una corrida como exitosa y automatizar verificaciones en `D04`/`D05`. |
| `RSK-05` | **Alcance excesivo (*scope creep*):** intentar agregar predicción meteorológica, pronóstico de precios, sensores IoT o interfaces complejas que impidan cerrar la rebanada vertical `DEC-01` a tiempo. | Alto | Media | Cumplir estrictamente las exclusiones de `PROJECT_CHARTER.md`, priorizar el cierre de punta a punta de `DEC-01` en `D04` y exigir autorización formal (`DECISION_LOG.md`) para cualquier ampliación. |
| `RSK-06` | **Falta de reproducibilidad experimental:** resultados de corridas evolutivas imposibles de replicar por semillas (`seed`) no controladas o cambios no registrados en los catálogos de la `Base de Conocimiento`. | Alto | Baja | Exigir `seed` explícita y `data_vintage` en cada ejecución, registrar todas las corridas en `03_MEMORY/experiments/EXPERIMENT_LOG.csv` y verificar determinismo mediante pruebas repetidas en `D04` y `D05`. |
| `RSK-07` | **Selección prematura o injustificada de stack tecnológico:** adoptar herramientas antes de evaluar requisitos del problema, generando deuda técnica o justificaciones a posteriori. | Medio | Baja | Mantener el stack estrictamente abierto hasta elaborar y aprobar la matriz comparativa en `D02` y el diseño detallado en `D03`. |

---

## Criterio de Revisión

Este registro debe revisarse al cierre de cada entregable (`D01`–`D06`) y actualizarse cuando surjan nuevos riesgos técnicos, agronómicos o de calendario durante la experimentación.
