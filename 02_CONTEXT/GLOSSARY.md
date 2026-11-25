# Glosario Técnico y Agronómico — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`

---

## 1. Vocabulario de Inteligencia Artificial y Algoritmos Genéticos

| Término | Definición en el contexto de SAGE |
| :--- | :--- |
| **Algoritmo Genético (AG)** | Metaheurística evolutiva inspirada en la selección natural que optimiza una población de planes candidatos mediante evaluación de *Fitness*, selección, cruce y mutación a lo largo de generaciones. |
| **Cromosoma (Individuo)** | Representación estructurada de un plan agrícola completo a 5 años (10 ciclos `PV`/`OI`) para todas las parcelas del predio piloto (3 a 10 parcelas). |
| **Gen** | Unidad básica de decisión dentro del cromosoma correspondiente a una celda `(parcela, ciclo)` que codifica el tipo de cultivo y la asignación de riego. |
| **Alelo** | Valor concreto asignado a un gen dentro de su dominio válido (por ejemplo, cultivo `1` = Maíz y un nivel de riego específico para ese ciclo). |
| **Función Fitness** | Función escalar o agregada que evalúa la calidad global de un cromosoma combinando las 4 Variables a Optimizar (costo, producción, nitrógeno del suelo y desperdicio/estrés hídrico) junto con penalizaciones por violar restricciones como `N <= 0`. |
| **Cruce (*Crossover*)** | Operador genético que combina segmentos de dos individuos padres para generar descendencia heredando patrones de rotación y riego potencialmente superiores. |
| **Mutación** | Operador que altera aleatoriamente uno o más alelos de un cromosoma (con probabilidad controlada) para introducir variación y evitar el estancamiento genético. |
| **Poda / Selección de sobrevivientes** | Mecanismo que descarta individuos de bajo desempeño o redundantes al formar la siguiente generación, preservando presión selectiva y calidad poblacional (pudiendo combinarse con elitismo acotado). |
| **Óptimo local** | Solución mejor que sus vecinas inmediatas en el espacio de búsqueda, pero inferior a soluciones globalmente mejores; riesgo principal ante convergencia prematura (`RSK-01`). |
| **Convergencia del Fitness** | Evolución por generación de las métricas de mejor, promedio y peor *Fitness* de la población; evidencia central del aprendizaje evolutivo del AG. |
| **Semilla (`seed`)** | Valor entero inicial del generador pseudoaleatorio que garantiza reproducibilidad exacta de una corrida experimental del AG. |
| **DSS Prescriptivo** | Sistema de Apoyo a la Decisión orientado a recomendar cursos de acción óptimos o cuasi-óptimos bajo restricciones dadas (`DEC-01`, `DEC-02`), a diferencia de un sistema predictivo que estima eventos futuros inciertos. |

---

## 2. Vocabulario Agronómico y de Dominio

| Término | Definición en el contexto de SAGE |
| :--- | :--- |
| **Barbecho / Descanso (código `0`)** | Ciclo en el que una parcela permanece sin siembra comercial para permitir la recuperación natural del suelo (incremento/estabilización de nitrógeno) y reducción de costos e insumos hídricos. |
| **Ciclo `PV` (Primavera-Verano)** | Primer ciclo agrícola semestral de cada año del horizonte de planificación (ciclos `1, 3, 5, 7, 9`), con condiciones hídricas y de cultivos propios de la temporada cálida. |
| **Ciclo `OI` (Otoño-Invierno)** | Segundo ciclo agrícola semestral de cada año del horizonte de planificación (ciclos `2, 4, 6, 8, 10`), con requerimientos hídricos y aptitud de cultivos propios de la temporada fresca. |
| **Rotación de cultivos** | Sucesión planificada de cultivos distintos (incluyendo leguminosas como Frijol y descansos en Barbecho) sobre una misma parcela a lo largo de varios ciclos para conservar fertilidad y sostener rendimiento. |
| **Balance de nitrógeno (`N`)** | Variación acumulada del nitrógeno disponible en el suelo de cada parcela ciclo tras ciclo, resultante de la extracción por cultivos demandantes, la fijación biológica (Frijol) y la recuperación en Barbecho; debe mantenerse estrictamente en `N > 0`. |
| **Estrés hídrico** | Déficit de agua que ocurre cuando el riego asignado a una parcela es inferior al requerimiento hídrico real del cultivo en ese ciclo, penalizando el rendimiento y el *Fitness*. |
| **Desperdicio de agua** | Exceso de riego por encima del requerimiento hídrico del cultivo en el ciclo, que eleva el costo operativo y es penalizado en la cuarta Variable a Optimizar (`VO-4`). |
| **Línea base agrícola** | Plan de referencia sin optimización evolutiva (monocultivo continuo y/o planificación empírica manual con riego fijo) utilizado para medir la ganancia real de SAGE. |
| **`Base de Conocimiento` estática** | Conjunto de catálogos agronómicos y parámetros ambientales sintéticos de referencia (`crops_catalog`, `env_params`) que gobiernan el comportamiento del modelo sin conexión a pronósticos externos. |
| **`data_vintage`** | Fecha o etiqueta de versión que identifica la vigencia de los catálogos sintéticos utilizados en una corrida para asegurar trazabilidad e incertidumbre explícita. |
