# Contexto General del Proyecto — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo
- **Nivel epistemológico:** `VERIFIED` (síntesis vinculada a fuentes canónicas)

---

## 1. Resumen Compacto y Estable

**SAGE** es un **Sistema de Apoyo a la Decisión (DSS) prescriptivo** basado en **Algoritmos Genéticos (AG)** desarrollado como proyecto final académico para la materia *Fundamentos de Inteligencia Artificial* (Ingeniería en TI e Innovación Digital).

- **Qué optimiza:** planes espaciotemporales de rotación de cultivos y asignación de riego para una unidad agrícola de **3 a 10 parcelas** durante **5 años (10 ciclos semestrales `PV`/`OI`)**.
- **Qué NO hace:** no predice clima ni precios de mercado, no usa sensores IoT en tiempo real y no procesa datos personales (PII), PHI ni secretos reales.
- **Variables de Decisión (VD):** tipo de cultivo (`0` Barbecho/Descanso, `1` Maíz, `2` Frijol, `3` Sorgo, `4` Avena/Trigo), fecha (ciclo `PV`/`OI`), riego y parcela.
- **Variables a Optimizar (VO):** minimizar costo operativo, maximizar producción, preservar/maximizar nitrógeno del suelo (`N > 0`) y minimizar desperdicio de agua / estrés hídrico.
- **Decisiones apoyadas:** `DEC-01` *(rebanada vertical prioritaria)* y `DEC-02` *(selección entre los 3 mejores individuos distintos)*.
- **Salidas obligatorias:** gráfica de convergencia del *Fitness* (mejor, promedio, peor por generación) + representación tabular y visual de los **3 mejores individuos** (calendario parcela × ciclo, evolución de nitrógeno, balance costo/producción y balance hídrico).

---

## 2. Principios Operativos No Negociables

1. **Decisión primero (DSS):** SAGE apoya al humano; no sustituye el criterio del administrador agrícola ni del agrónomo.
2. **Costo del error asimétrico e incertidumbre explícita:** toda salida expone su `data_vintage`, su `seed`, la comparación contra la línea base y la advertencia de parámetros estáticos.
3. **Separación estricta de capas:** `00_GOVERNANCE/`, `01_AGENT/`, `02_CONTEXT/`, `03_MEMORY/` y `04_RESEARCH/` cumplen responsabilidades disjuntas.
4. **Fase 0 de solo inspección:** ningún agente modifica archivos sin completar Fase 0 y contar con autorización explícita o `ACTIVE_TASK.yaml` (`authorized: true`).
5. **Inmutabilidad y trazabilidad epistemológica:** `DECISION_LOG.md` es solo anexar; toda afirmación se etiqueta (`VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN`, `CONTRADICTED`).
6. **Rebanada vertical temprana:** cerrar `DEC-01` de punta a punta en `D04` antes de escalar.
7. **Stack tecnológico abierto hasta `D02`/`D03`:** cero decisiones tecnológicas anticipadas ni justificaciones a posteriori.

---

## 3. Enlaces a Fuentes Canónicas

- Acta constitutiva y exclusiones: `00_GOVERNANCE/PROJECT_CHARTER.md`
- Especificación DSS (`DEC-01` y `DEC-02`): `00_GOVERNANCE/DECISION_SPEC.md`
- Reglas de trabajo y control de calidad: `00_GOVERNANCE/WORKING_RULES.md`
- Registro de riesgos: `00_GOVERNANCE/RISK_REGISTER.md`
- Decisión fundacional inmutable (`D-0001`): `03_MEMORY/decisions/DECISION_LOG.md`
- Estado vivo y hoja de ruta: `02_CONTEXT/CURRENT_STATE.md`, `03_MEMORY/state/PROJECT_STATUS.yaml`, `04_RESEARCH/research_protocol.md`
