# Lecciones Aprendidas — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Política:** Registro cronológico acumulativo (`L-0001`, `L-0002`, ...)
- **Fecha de línea base:** `2026-11-23`

---

## `L-0001` — Delimitación prescriptiva y equilibrio multiobjetivo para evitar planes destructivos

- **Fecha:** `2026-11-23`
- **Fase / Origen:** Definición de gobernanza inicial (`D-0001`, `PROJECT_CHARTER.md`, `DECISION_SPEC.md`)
- **Nivel epistemológico:** `VERIFIED`
- **Categoría:** Formulación del problema y diseño DSS

### Hallazgo
Durante la estructuración conceptual de SAGE se confirmó que mezclar expectativas de predicción (clima o precios) con optimización combinatoria diluye el valor del Algoritmo Genético e introduce dependencias incontrolables. Asimismo, formular una función objetivo centrada únicamente en maximizar ingresos a corto plazo conduce sistemáticamente a soluciones destructivas (monocultivos continuos de alto retorno que agotan el nitrógeno del suelo hasta `N <= 0` y desperdician o subasignan riego).

### Acción Preventiva Incorporada
1. Fijar explícitamente en `PROJECT_CHARTER.md` y `D-0001` que SAGE es un **DSS prescriptivo / de optimización** sobre catálogos estáticos, y **no** un sistema predictivo.
2. Incluir las cuatro Variables a Optimizar (**Costo**, **Producción**, **Nivel de Nutrientes del Suelo con umbral `N > 0`** y **Desperdicio de Agua / Estrés Hídrico**) desde el diseño base (`DEC-01`), junto con el análisis comparativo de **3 mejores individuos distintos** (`DEC-02`) para hacer visibles los *trade-offs* antes de elegir el plan final.
3. Aplicar esta restricción de manera obligatoria en el diseño de la función *Fitness* (`D03`) y en la validación de sensibilidad (`D05`).

---

## `L-0002` — Sensibilidad a la tasa de mutación en cromosomas acoplados cultivo-riego

- **Fecha:** `2026-11-23`
- **Fase / Origen:** Campaña experimental `D05` (`EXP-001`, `EXP-002`, `EXP-003` en `EXPERIMENT_LOG.csv`)
- **Nivel epistemológico:** `VERIFIED`
- **Categoría:** Calibración del Algoritmo Genético

### Hallazgo
En la campaña `D05`, elevar la tasa de mutación a `14%` (`EXP-003`) destruyó de forma recurrente la sincronización fina entre el cultivo elegido y su nivel óptimo de riego, degradando el desvío hídrico promedio a `156.00 mm` y reduciendo la utilidad neta a `96,579.00 USD` (`Fitness 0.6343`). En contraste, ampliar la población (`140`) con una mutación moderada (`5%`) y elitismo acotado (`6`) en `EXP-002` permitió bajar el desvío hídrico a apenas `3.00 mm` y elevar la utilidad neta a `192,628.75 USD` (`Fitness 0.7695`).

### Acción Preventiva Incorporada
1. Adoptar mutación baja-moderada (`0.05`–`0.08`) con tamaño poblacional `>= 120` como rango recomendado para cromosomas de 50 genes `(crop_id, irrigation_level)`.
2. Mantener la comparación multi-experimento en `EXPERIMENT_LOG.csv` para justificar empíricamente los hiperparámetros en la defensa académica.

---

## `L-0003` — Validación de líneas base sobre parcelas heterogéneas con bajo nitrógeno inicial

- **Fecha:** `2026-11-23`
- **Fase / Origen:** Pruebas unitarias de `D04` (`09_VALIDATION/test_evaluator_and_baselines.py`)
- **Nivel epistemológico:** `VERIFIED`
- **Categoría:** Validación agronómica y pruebas

### Hallazgo
La primera propuesta de rotación empírica manual (`[Maíz, Barbecho, Sorgo, Frijol, Maíz, Barbecho, Sorgo, Avena/Trigo, Frijol, Barbecho]`) resultaba factible para parcelas ricas en nitrógeno (`P1`, `P3`), pero agotaba a `P4` (`N_0 = 40 kg/ha`) hasta `-6.0 kg/ha` al encadenar Sorgo (`-20`) y Avena/Trigo (`-18`). La prueba automatizada detectó inmediatamente esta infactibilidad oculta.

### Acción Preventiva Incorporada
1. Ajustar el patrón de la línea base empírica (`[Maíz, Barbecho, Sorgo, Frijol, Maíz, Barbecho, Frijol, Avena/Trigo, Sorgo, Barbecho]`) para garantizar un *benchmark* manual genuinamente factible (`N mín = 6.0 kg/ha > 0`) contra el cual comparar de manera justa al Algoritmo Genético.
2. Evaluar siempre `min_nitrogen_any_cycle` sobre la totalidad de parcelas y ciclos, no solo el promedio final.

---

## `L-0004` — Archivo histórico y filtro de distancia de Hamming para evitar Top-3 redundante

- **Fecha:** `2026-11-23`
- **Fase / Origen:** Diseño `D03` y validación `D05` (`DEC-02`)
- **Nivel epistemológico:** `VERIFIED`
- **Categoría:** Apoyo a la decisión (`DEC-02`) y mitigación de `RSK-01`

### Hallazgo
Al final de 180 generaciones, los mejores individuos de la población convergen a variantes muy cercanas entre sí. Sin un archivo histórico de candidatos únicos y un umbral mínimo de distancia de Hamming (`>= 10` alelos en `EXP-002`), el reporte Top-3 tendería a mostrar tres planes casi idénticos sin verdaderos compromisos (*trade-offs*).

### Acción Preventiva Incorporada
1. Implementar archivo histórico de individuos únicos + selección voraz con distancia de Hamming mínima (`select_distinct_top_k`), logrando distancias reales de `10`, `11` y `13` alelos con perfiles distintos en utilidad neta, valor bruto y regeneración de nitrógeno.
