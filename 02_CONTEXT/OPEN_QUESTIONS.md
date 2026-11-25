# Preguntas Abiertas — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.2.0`
- **Fecha de actualización:** `2026-11-23`
- **Estado general:** Todas las incógnitas (`OQ-01`–`OQ-08`) cerradas y aprobadas formalmente por Sayd Quevedo en **`D-0005`**.

---

## Registro Consolidado de Incógnitas Resueltas

| ID | Pregunta abierta | Impacto | Entregable / Decisión que la cerró | Estado |
| :--- | :--- | :--- | :--- | :--- |
| `OQ-01` | ¿Cuáles serán los valores exactos de referencia del catálogo agronómico sintético (`0` Barbecho, `1` Maíz, `2` Frijol, `3` Sorgo, `4` Avena/Trigo) para costo, rendimiento, delta de nitrógeno (`ΔN`) y requerimiento hídrico en `PV` y `OI`? | Alto | `D01` + `D-0005` (`05_DATA/reference/crops_catalog.json` en `MXN`) | `VERIFIED` (Cerrada y aprobada) |
| `OQ-02` | ¿Qué escenario exacto de línea base y qué número exacto de parcelas piloto se usarán como *benchmark* oficial? | Alto | `D01` / `D04` + `D-0005` (`PILOT_5P_10C`, Monocultivo Maíz + Rotación Empírica fija `300 mm`) | `VERIFIED` (Cerrada y aprobada) |
| `OQ-03` | ¿Qué lenguaje de programación, enfoque del AG, formato de catálogos y herramienta de graficación ofrecen la mejor reproducibilidad? | Alto | `D02` (`D-0002` + `D-0004`: Python 3.12 + NumPy + Pandas + Matplotlib + PyYAML + pytest en `BACKEND/`) | `VERIFIED` (Cerrada y aprobada) |
| `OQ-04` | ¿La variable de decisión de riego se codificará como nivel discreto o continuo? | Alto | `D03` + `D-0005` (5 niveles discretos `0..4` -> `0, 150, 300, 450, 600 mm`) | `VERIFIED` (Cerrada y aprobada) |
| `OQ-05` | ¿Cómo se normalizarán las 4 VO y qué pesos/penalizaciones garantizarán `N > 0` sin aplastar la exploración? | Crítico | `D03` / `D05` + `D-0005` (pesos `0.38/0.22/0.22/0.18` y penalizaciones `EXP-002` `3.50/1.10/0.85` + `-0.50`) | `VERIFIED` (Cerrada y aprobada) |
| `OQ-06` | ¿Qué métrica de distancia estructural definirá que los 3 mejores individuos de `DEC-02` son distintos? | Medio | `D03` / `D05` + `D-0005` (Hamming `>= 10` sobre 100 alelos; distancias reales `10`, `11` y `13`) | `VERIFIED` (Cerrada y aprobada) |
| `OQ-07` | ¿Se incorporará un tope global opcional de agua o presupuesto por ciclo además de las restricciones por parcela? | Medio | `D01` / `D03` + `D-0005` (excluido en v1.0.0 para preservar `ASM-04` y claridad de `DEC-01`) | `VERIFIED` (Cerrada y aprobada) |
| `OQ-08` | ¿Qué moneda de referencia y tope de nitrógeno edáfico se utilizarán en los reportes finales? | Bajo | `D-0005` (moneda convertida y verificada en **MXN** con escala realista `20 MXN = 1 USD`; tope `N_max = 120 kg/ha`) | `VERIFIED` (Cerrada y aprobada) |
