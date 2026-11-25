# Registro Inmutable de Decisiones de Gobernanza — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Política:** Append-only (solo anexar) — `03_MEMORY/MEMORY_POLICY.md`
- **Responsable de aprobación:** Sayd Quevedo

---

## Regla de Uso

Este archivo registra **exclusivamente decisiones de gobernanza, alcance, arquitectura, selección de stack tecnológico, aprobación de entregables y cambios de política** del proyecto SAGE.

- **NO** registrar aquí salidas operativas del Algoritmo Genético ni planes agrícolas seleccionados en corridas experimentales (`DEC-01`/`DEC-02`); esas salidas pertenecen a `03_MEMORY/experiments/EXPERIMENT_LOG.csv` y `11_OUTPUTS/`.
- Los identificadores siguen secuencia estricta `D-0001`, `D-0002`, `D-0003`, ...

---

## Asiento `D-0001`

- **ID:** `D-0001`
- **Fecha:** `2026-11-23`
- **Estado:** `aprobada`
- **Autor / Responsable de aprobación:** Sayd Quevedo
- **Nivel epistemológico:** `VERIFIED`
- **Título:** Línea base constitucional, alcance prescriptivo, variables del problema y stack abierto para SAGE

### Contexto
Se establece la línea base documental previa al desarrollo del proyecto final académico **SAGE (Sistema Agrícola de Genética Evolutiva)** para la materia *Fundamentos de Inteligencia Artificial* (Ingeniería en TI e Innovación Digital), con el objetivo de garantizar gobernanza *AI-Ready*, trazabilidad epistemológica y disciplina de modelado antes de escribir código.

### Decisión Aprobada
1. **Naturaleza y propósito:** SAGE se define formalmente como un **Sistema de Apoyo a la Decisión (DSS) de naturaleza prescriptiva / optimización** basado en Algoritmos Genéticos (AG). **NO es un sistema predictivo** (no pronostica clima ni precios) y apoya al decisor sin sustituir el criterio humano.
2. **Ámbito operativo:** Unidad agrícola de **3 a 10 parcelas** en un horizonte de **5 años** divididos en **10 ciclos semestrales** alternados: **Primavera-Verano (PV)** y **Otoño-Invierno (OI)**.
3. **Variables de Decisión (VD — genes del cromosoma):**
   - `VD-1`: Tipo de cultivo (`0` = Barbecho/Descanso, `1` = Maíz, `2` = Frijol, `3` = Sorgo, `4` = Avena/Trigo).
   - `VD-2`: Fecha (ciclo agrícola `PV` / `OI`).
   - `VD-3`: Riego (volumen o frecuencia asignada).
   - `VD-4`: Parcela.
4. **Variables a Optimizar (VO):**
   - `VO-1`: Costo operativo total (minimizar).
   - `VO-2`: Producción total cosechada en toneladas / valor bruto (maximizar).
   - `VO-3`: Nivel de nutrientes del suelo, preservando nitrógeno por encima del umbral crítico `N > 0` (maximizar/preservar).
   - `VO-4`: Desperdicio de agua / estrés hídrico como desviación entre riego aplicado y requerimiento hídrico del cultivo en el ciclo (minimizar).
5. **Decisiones apoyadas y prioridad:**
   - `DEC-01` *(rebanada vertical prioritaria)*: Planificación espaciotemporal de rotación de cultivos y asignación de riego por parcela y ciclo (`PV`/`OI`) a 5 años.
   - `DEC-02` *(secundaria)*: Selección del plan operativo final entre los **3 mejores individuos** distintos generados por el AG, evaluando *trade-offs* financieros, edáficos e hídricos.
6. **Salidas obligatorias:** Gráfica de convergencia del *Fitness* (mejor, promedio y peor por generación) + representación tabular y visual de los **3 mejores individuos** distintos (calendario parcela × ciclo, evolución de nitrógeno, balance costo/producción y balance hídrico).
7. **Datos, privacidad y evidencia:** Operación exclusiva con datos sintéticos y catálogos agronómicos estáticos (`Base de Conocimiento`); cero PII, cero PHI y cero secretos reales. Evidencia estrictamente técnica (código, corridas reproducibles con `seed`, pruebas, métricas y gráficas); no incluye encuestas ni trabajo de campo.
8. **Stack tecnológico:** Se mantiene **ABIERTO** (`TBD_IN_D02`). Queda prohibido asumir lenguaje de programación, librerías de AG, base de datos o framework de interfaz antes de su evaluación y aprobación formal en `D02`/`D03`.

### Alternativas Descartadas
- Construir un sistema híbrido predictivo de clima/precios: descartado por riesgo de *scope creep* (`RSK-05`) y desenfoque del objetivo central de optimización evolutiva.
- Fijar lenguaje y librerías desde el acta constitutiva: descartado para evitar justificaciones a posteriori y asegurar una selección fundamentada en `D02`.
- Optimizar únicamente utilidad económica sin modelar nitrógeno (`N > 0`) ni estrés hídrico: descartado porque genera soluciones agronómicamente destructivas (`L-0001`).

### Consecuencias y Trazabilidad
- Quedan fijadas las fuentes canónicas en `00_GOVERNANCE/`, la capa de agentes en `01_AGENT/`, el contexto en `02_CONTEXT/`, el estado inicial en `03_MEMORY/state/` y la hoja de ruta `D01`–`D06` en `04_RESEARCH/research_protocol.md`.
- El inicio del entregable `D01` requerirá el asiento de autorización `D-0002` y la activación de `03_MEMORY/state/ACTIVE_TASK.yaml`.

---

## Asiento `D-0002`

- **ID:** `D-0002`
- **Fecha:** `2026-11-23`
- **Estado:** `aprobada`
- **Autor / Responsable de aprobación:** Sayd Quevedo (ejecución autónoma autorizada end-to-end `D01`–`D06`)
- **Nivel epistemológico:** `VERIFIED`
- **Título:** Aprobación de formulación `D01`, selección formal de stack tecnológico (`D02`) y autorización del ciclo `D01`–`D06`

### Contexto
Con la línea base documental `D-0001` validada y la autorización explícita de Sayd Quevedo para ejecutar de forma autónoma el ciclo completo `D01`–`D06`, se cierra `D01` (formulación matemática, escenario sintético `PILOT_5P_10C` en `05_DATA/reference/` y líneas base) y se realiza la evaluación comparativa objetiva de stack en `04_RESEARCH/D02/01_SPEC.md` resolviendo `OQ-03`.

### Decisión Aprobada
1. **Stack tecnológico seleccionado (cierra el estado abierto de `D-0001`):**
   - **Lenguaje y motor evolutivo:** **Python 3.12+** con **NumPy** implementando un motor de Algoritmo Genético modular propio en `08_APPLICATION/sage/` con determinismo exacto (`numpy.random.Generator` / `PCG64`).
   - **Datos y análisis tabular:** catálogos JSON en `05_DATA/reference/` (validados en modo *fail-fast*), configuración YAML (**PyYAML**) y exportación tabular con **Pandas**.
   - **Visualización:** **Matplotlib** (backend no interactivo `Agg`) para exportar las gráficas obligatorias a `11_OUTPUTS/`.
   - **Pruebas:** **pytest** en `09_VALIDATION/`.
   - **Interfaz:** CLI local reproducible (`python -m sage.cli`), sin sobreingeniería de servicios externos.
2. **Escenario piloto y modelo de riego:** Se fija el escenario piloto `PILOT_5P_10C` (5 parcelas heterogéneas × 10 ciclos `PV`/`OI`) y la codificación discreta de riego en 5 niveles (`0..4` -> `0, 150, 300, 450, 600 mm`), etiquetando los parámetros agronómicos y pesos iniciales como `ASSUMPTION` sujetos a validación final humana.

### Alternativas Descartadas
- Librerías evolutivas de caja negra (DEAP/PyGAD): descartadas para conservar control y transparencia total de operadores genéticos y diversidad Top-3 (`DEC-02`).
- Node.js/TypeScript o Java/C#: descartadas por mayor fricción para graficación científica local y pruebas numéricas rápidas.

### Consecuencias y Trazabilidad
- Se crea `requirements.txt` y se actualizan `config/environment.example.yaml`, `.env.example` y `02_CONTEXT/TECHNICAL_CONTEXT.md`.
- Se habilita la ejecución secuencial de `D03`, `D04`, `D05` y `D06` bajo las reglas de `00_GOVERNANCE/WORKING_RULES.md`.

---

## Asiento `D-0003`

- **ID:** `D-0003`
- **Fecha:** `2026-11-23`
- **Estado:** `aprobada`
- **Autor / Responsable de aprobación:** Sayd Quevedo (bajo autorización autónoma end-to-end `D01`–`D06`)
- **Nivel epistemológico:** `VERIFIED`
- **Título:** Cierre técnico de `D03`–`D06`, validación de rebanada vertical `DEC-01` y adopción de `EXP-002` como calibración de referencia `DEC-02`

### Contexto
Tras completar el diseño `D03`, implementar la rebanada vertical `DEC-01` en `08_APPLICATION/sage/`, aprobar `11/11` pruebas automatizadas en `09_VALIDATION/` (`D04`), ejecutar la campaña experimental `EXP-001`–`EXP-003` en `D05` y consolidar la documentación final en `10_DOCUMENTATION/SAGE_FINAL_REPORT.md` (`D06`), se fija la configuración experimental de referencia para la entrega académica.

### Decisión Aprobada
1. **Configuración de referencia (`EXP-002`):** `population_size=140`, `generations=180`, `crossover_rate=0.88`, `mutation_rate=0.05`, `tournament_size=5`, `elitism_count=6`, `seed=2026`, `min_top3_hamming_distance=10` y penalizaciones estrictas (`nitrogen=3.50`, `season=1.10`, `monoculture=0.85`).
2. **Resultados verificados:** `SAGE_Top_1` obtiene `Fitness=0.7695`, utilidad neta de `192,628.75 USD`, nitrógeno final promedio de `73.60 kg/ha` (`N mín=36.00 kg/ha`), desvío hídrico de `3.00 mm` y `0/0/0` violaciones, superando ampliamente a `Baseline_Rotacion_Empirica` (`Fitness=0.5574`, utilidad `75,186.00 USD`, desvío `195.00 mm`) y a `Baseline_Monocultivo` (`Fitness=-4.7114`).
3. **Salidas obligatorias consolidadas:** Todas las gráficas PNG y reportes CSV/JSON/Markdown de `EXP-002` quedan publicados en `11_OUTPUTS/` y registrados en `03_MEMORY/experiments/EXPERIMENT_LOG.csv`.

### Consecuencias y Trazabilidad
- El proyecto queda listo para revisión final de los supuestos marcados como `ASSUMPTION` en `02_CONTEXT/OPEN_QUESTIONS.md` por Sayd Quevedo.
- `03_MEMORY/state/ACTIVE_TASK.yaml` se devuelve a `authorized: false` para restaurar la compuerta segura de Fase 0 en futuras sesiones.

---

## Asiento `D-0004`

- **ID:** `D-0004`
- **Fecha:** `2026-11-23`
- **Estado:** `aprobada`
- **Autor / Responsable de aprobación:** Sayd Quevedo
- **Nivel epistemológico:** `VERIFIED`
- **Título:** Refactor estructural: centralización del código fuente del backend en la carpeta raíz `BACKEND/`

### Contexto
Para mejorar la claridad operativa y separar de forma inmediata el código fuente ejecutable del backend respecto a las capas documentales numeradas, el responsable del proyecto autorizó migrar el código Python desde `08_APPLICATION/` hacia una carpeta raíz dedicada `BACKEND/`.

### Decisión Aprobada
1. **Nueva ubicación canónica del código fuente:** todo el paquete `sage/` y `requirements.txt` se centralizan en `BACKEND/` (`BACKEND/sage/` y `BACKEND/requirements.txt`).
2. **Retiro de `08_APPLICATION/`:** se elimina la carpeta `08_APPLICATION/` una vez completada la migración para evitar duplicación de fuentes.
3. **Actualización de pruebas, configuración y documentación:** `09_VALIDATION/conftest.py`, `README.md`, `10_DOCUMENTATION/SAGE_FINAL_REPORT.md`, `config/environment.example.yaml` y `02_CONTEXT/TECHNICAL_CONTEXT.md` apuntan a `BACKEND/` (`PYTHONPATH="BACKEND"`).

### Consecuencias y Trazabilidad
- No altera la lógica algorítmica, la Base de Conocimiento (`05_DATA/reference/`) ni los resultados experimentales registrados en `D-0003`.
- Verificado mediante ejecución limpia de `pytest 09_VALIDATION -v` (`11/11` pruebas) y verificación de CLI `python -m sage.cli --help` con `PYTHONPATH="BACKEND"`.

---

## Asiento `D-0005`

- **ID:** `D-0005`
- **Fecha:** `2026-11-23`
- **Estado:** `aprobada`
- **Autor / Responsable de aprobación:** Sayd Quevedo
- **Nivel epistemológico:** `VERIFIED`
- **Título:** Aprobación definitiva de parámetros (`OQ-01`–`OQ-08`), conversión de moneda de referencia a **MXN** y cierre aprobado de `D06`

### Contexto
Tras la revisión final del proyecto SAGE por Sayd Quevedo, se aprueban explícitamente los parámetros agronómicos, la discretización de riego, los pesos/penalizaciones de la función *Fitness* y el alcance v1.0.0 (`OQ-01`, `OQ-04`, `OQ-05`, `OQ-07`), solicitando expresar todas las métricas, catálogos, reportes y gráficas en **Pesos Mexicanos (MXN)** (`OQ-08`) con cierre formal de `D06`.

### Decisión Aprobada
1. **Conversión a MXN (escala exacta `20 MXN = 1 USD`):** se actualizan `05_DATA/reference/crops_catalog.json`, `05_DATA/reference/env_params.json` (`currency: "MXN"`, agua `9.0 MXN/(mm·ha)`, escalas `44,000` / `19,000 MXN/ha/ciclo`) y `BACKEND/sage/`, preservando intacta la proporcionalidad matemática y los puntajes de *Fitness* (`EXP-002`: `Fitness=0.7695`, utilidad neta `SAGE_Top_1 = 3,852,575.00 MXN` vs. `Baseline_Rotacion_Empirica = 1,503,720.00 MXN`).
2. **Cierre de preguntas abiertas:** `OQ-01` a `OQ-08` quedan formalmente cerradas y verificadas en `02_CONTEXT/OPEN_QUESTIONS.md`.
3. **Aprobación definitiva del proyecto (`D06`):** `D06` pasa de `in_review` a `approved` y `pending_approval` cambia a `false` en `03_MEMORY/state/PROJECT_STATUS.yaml`.

### Consecuencias y Trazabilidad
- Todas las gráficas PNG y reportes CSV/JSON/Markdown en `11_OUTPUTS/`, así como `03_MEMORY/experiments/EXPERIMENT_LOG.csv` y `10_DOCUMENTATION/SAGE_FINAL_REPORT.md`, quedan regenerados y verificados en **MXN** con `11/11` pruebas `pytest` en verde.

---

## Nota de Inmutabilidad

> **INMUTABILIDAD ESTRICTA:** Ningún agente ni colaborador debe modificar, resumir ni eliminar asientos ya registrados en este archivo (como `D-0001`). Toda actualización, ampliación o revocación futura deberá añadirse al final como un nuevo asiento numerado secuencialmente (`D-0002`, `D-0003`, ...) referenciando explícitamente el ID que complementa o reemplaza.
