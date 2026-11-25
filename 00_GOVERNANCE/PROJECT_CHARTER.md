# Acta Constitutiva del Proyecto — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Estado:** Aprobado (Línea base `D-0001`)
- **Fecha de línea base:** `2026-11-23`
- **Autor / Responsable de aprobación:** Sayd Quevedo
- **Contexto académico:** Proyecto final para la materia *Fundamentos de Inteligencia Artificial* (Ingeniería en TI e Innovación Digital)
- **Nivel epistemológico del documento:** `VERIFIED` (fuente de autoridad inmutable de alcance y propósito)

---

## 1. Qué es SAGE

**SAGE (Sistema Agrícola de Genética Evolutiva)** es un **Sistema de Apoyo a la Decisión (DSS)** de naturaleza estrictamente **prescriptiva y de optimización**, basado en **Algoritmos Genéticos (AG)**, diseñado para planificar de forma espaciotemporal la rotación de cultivos y la asignación de riego en unidades agrícolas de múltiples parcelas.

**Delimitación fundamental de naturaleza:**
- SAGE **es** un sistema prescriptivo de optimización combinatoria multiobjetivo: explora el espacio de planes posibles para proponer calendarios agrícolas viables, rentables y sostenibles.
- SAGE **NO es** un sistema predictivo: no pronostica clima, precipitaciones, plagas ni volatilidad de precios de mercado; opera sobre catálogos agronómicos y parámetros económicos de referencia estáticos (`Base de Conocimiento`).

---

## 2. Problema que Resuelve

En unidades agrícolas multiparcela, la planificación manual o empírica basada en monocultivo suele optimizar únicamente el ingreso de corto plazo, lo que provoca:

1. **Agotamiento progresivo del suelo:** caída del nivel de nitrógeno (`N`) por siembra repetida de cultivos extractivos sin rotación con leguminosas ni periodos de barbecho.
2. **Ineficiencia hídrica:** sobre-riego (desperdicio de agua y costos innecesarios) o sub-riego (estrés hídrico y merma de rendimiento) por desalineación con la demanda del cultivo en cada temporada.
3. **Explosión combinatoria:** evaluar manualmente combinaciones de cultivo y riego para múltiples parcelas (piloto base: 3 a 10 parcelas) a lo largo de 5 años divididos en 10 ciclos semestrales —**Primavera-Verano (PV)** y **Otoño-Invierno (OI)**— supera la capacidad de análisis heurístico manual.

SAGE resuelve este problema formulando el plan agrícola como un cromosoma evolutivo cuyas **Variables de Decisión (VD)** son:
1. **Tipo de cultivo:** `0` = Barbecho/Descanso, `1` = Maíz, `2` = Frijol, `3` = Sorgo, `4` = Avena/Trigo.
2. **Fecha:** ciclo agrícola semestral (`PV` / `OI`) en un horizonte de 10 ciclos (5 años).
3. **Riego:** volumen o frecuencia hídrica asignada por parcela y ciclo.
4. **Parcela:** identificador de la unidad de tierra gestionada dentro del predio.

Y optimizando simultáneamente cuatro **Variables a Optimizar (VO)**:
1. **Costo:** minimizar el costo operativo total (semillas, insumos, mantenimiento, agua).
2. **Producción:** maximizar el rendimiento total cosechado (toneladas y valor bruto).
3. **Nivel de Nutrientes del Suelo:** maximizar y preservar el nitrógeno por encima del umbral crítico (`N > 0`).
4. **Desperdicio de Agua / Estrés Hídrico:** minimizar la desviación entre el riego aplicado y el requerimiento hídrico real del cultivo en ese ciclo.

---

## 3. Usuarios Objetivo

| Perfil de usuario | Rol operativo | Uso principal de SAGE |
| :--- | :--- | :--- |
| **Administrador agrícola** | Decisor operativo y financiero de la unidad productiva | Comparar los 3 mejores planes alternativos (`DEC-02`) evaluando costo, producción y sostenibilidad para elegir el plan operativo a ejecutar. |
| **Agrónomo** | Especialista técnico en suelos, rotación y manejo hídrico | Validar la coherencia agronómica de las secuencias de cultivo, verificar la evolución del nitrógeno (`N > 0`) y revisar la adecuación del riego por ciclo PV/OI. |
| **Evaluador académico** | Docente o revisor de *Fundamentos de Inteligencia Artificial* | Auditar la formulación del AG, la convergencia del *Fitness*, la reproducibilidad por semilla (`seed`), la comparación contra la línea base y la trazabilidad documental. |

---

## 4. Propósito y Principio DSS

El propósito de SAGE es generar, evaluar y presentar planes agrícolas de rotación y riego de alta calidad, con evidencia cuantitativa clara de sus compromisos (*trade-offs*), para respaldar dos decisiones estructuradas:
- `DEC-01` *(rebanada vertical prioritaria)*: planificación espaciotemporal de rotación de cultivos y asignación de riego por parcela y ciclo (PV/OI) a 5 años.
- `DEC-02` *(secundaria)*: selección del plan operativo final entre los **3 mejores individuos** distintos producidos por el AG.

> **Principio DSS no negociable:** SAGE apoya la toma de decisiones; **no sustituye el criterio humano** ni ejecuta acciones físicas automatizadas en campo.

---

## 5. Visión

Consolidar un sistema documental y técnico *AI-Ready*, auditable y reproducible que demuestre cómo los Algoritmos Genéticos resuelven un problema real de planificación agrícola sostenible multiobjetivo, manteniendo separación estricta entre gobernanza, datos de referencia, motor evolutivo y presentación de resultados.

---

## 6. Alcance del Proyecto

### 6.1 Incluye explícitamente
- Modelado prescriptivo de unidades agrícolas de **3 a 10 parcelas** en un horizonte de **5 años (10 ciclos semestrales PV/OI)**.
- Catálogo agronómico estático (`Base de Conocimiento`) con los 5 estados de cultivo (`0` Barbecho/Descanso, `1` Maíz, `2` Frijol, `3` Sorgo, `4` Avena/Trigo) y parámetros sintéticos de costo, rendimiento, nitrógeno y requerimiento hídrico.
- Diseño e implementación de un motor basado en Algoritmos Genéticos con control de reproducibilidad mediante semilla (`seed`).
- Comparación cuantitativa de las soluciones evolutivas frente a una **línea base explícita** (monocultivo y planificación empírica manual).
- Salidas obligatorias:
  1. **Gráfica de convergencia del *Fitness*** (mejor, promedio y peor individuo por generación).
  2. **Representación tabular y visual de los 3 mejores individuos** distintos (calendario parcela × ciclo, evolución de nitrógeno, balance costo/producción y balance hídrico).
- Evidencia estrictamente técnica: código fuente, corridas reproducibles con `seed`, registro de experimentos (`03_MEMORY/experiments/EXPERIMENT_LOG.csv`), pruebas y gráficas.
- Documentación y ejecución secuencial gobernada mediante entregables `D01` a `D06`.

### 6.2 Excluye explícitamente
- **Pronósticos predictivos:** modelos de clima, series de tiempo de precios de mercado, predicción de plagas o modelos de Machine Learning supervisado para predicción.
- **Sensores IoT y control en tiempo real:** telemetría de campo, estaciones meteorológicas en vivo o actuación automática sobre válvulas de riego.
- **Datos personales o sensibles:** cero PII (datos personales identificables), cero PHI (datos de salud) y cero secretos o credenciales reales en el repositorio.
- **Trabajo de campo y encuestas:** levantamiento de encuestas a productores, validación agronómica experimental en parcela física o estudios etnográficos.
- **Selección prematura de stack tecnológico:** queda prohibido fijar lenguaje de programación, librerías de AG, motor de persistencia o framework de interfaz antes de su justificación formal en `D02` y `D03`.

---

## 7. Referencias Canónicas

- Especificación de decisiones: `00_GOVERNANCE/DECISION_SPEC.md`
- Reglas operativas: `00_GOVERNANCE/WORKING_RULES.md`
- Registro de riesgos: `00_GOVERNANCE/RISK_REGISTER.md`
- Registro inmutable de decisiones de gobernanza: `03_MEMORY/decisions/DECISION_LOG.md` (`D-0001`)
- Protocolo de entregables `D01`–`D06`: `04_RESEARCH/research_protocol.md`
