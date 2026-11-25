# Memoria Consolidada del Proyecto — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.1.0`
- **Fecha de actualización:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo
- **Nivel epistemológico:** `VERIFIED`

---

## 1. Identidad y Estado Consolidado

SAGE es un **Sistema de Apoyo a la Decisión (DSS) prescriptivo** basado en **Algoritmos Genéticos (AG)** implementado para la materia *Fundamentos de Inteligencia Artificial* (Ingeniería en TI e Innovación Digital). Optimiza la rotación de cultivos (`0..4`) y la asignación de riego (`0..4` -> `0..600 mm`) en `5` parcelas (`18.0 ha`) a lo largo de `5` años (`10` ciclos `PV`/`OI`), preservando `N > 0` y maximizando el equilibrio multiobjetivo.

---

## 2. Decisiones Aprobadas Vigentes

| ID | Fecha | Estado | Resumen vinculante |
| :--- | :--- | :--- | :--- |
| `D-0001` | `2026-11-23` | `aprobada` | Línea base constitucional, alcance prescriptivo (no predictivo), 4 VD, 4 VO, `DEC-01`/`DEC-02`, datos sintéticos sin PII/PHI/secretos, evidencia técnica y stack abierto hasta `D02`. |
| `D-0002` | `2026-11-23` | `aprobada` | Aprobación de `D01` y selección formal del stack Python 3.12 + NumPy + Pandas + Matplotlib + PyYAML + pytest (`08_APPLICATION/sage/`, `09_VALIDATION/`). |
| `D-0003` | `2026-11-23` | `aprobada` | Cierre técnico de `D03`–`D06` (`11/11` pruebas pasando) y adopción de `EXP-002` (`seed=2026`, `Fitness=0.7695`, utilidad `192,628.75 USD`, `N final=73.60 kg/ha`, desvío hídrico `3.00 mm`) como referencia. |
| `D-0004` | `2026-11-23` | `aprobada` | Migración del código fuente de `08_APPLICATION/` a `BACKEND/` (`BACKEND/sage/` y `BACKEND/requirements.txt`) y actualización de rutas/pruebas a `PYTHONPATH="BACKEND"`. |
| `D-0005` | `2026-11-23` | `aprobada` | Cierre definitivo de `OQ-01`–`OQ-08`, conversión de catálogos, salidas y gráficas a **MXN** (`SAGE_Top_1 = 3,852,575.00 MXN`) y aprobación final de `D06` (`pending_approval: false`). |

---

## 3. Restricciones Persistentes y Referencias Clave

- Mantener la naturaleza estrictamente prescriptiva, cero PII/PHI/secretos, inmutabilidad de `DECISION_LOG.md` y Fase 0 obligatoria antes de cualquier cambio futuro.
- Informe final académico: `10_DOCUMENTATION/SAGE_FINAL_REPORT.md`
- Salidas gráficas y tabulares: `11_OUTPUTS/`
- Bitácora experimental: `03_MEMORY/experiments/EXPERIMENT_LOG.csv`
- Lecciones aprendidas (`L-0001`–`L-0004`): `03_MEMORY/lessons_learned/LESSONS.md`
- Estado máquina: `03_MEMORY/state/PROJECT_STATUS.yaml` y `03_MEMORY/state/ACTIVE_TASK.yaml`
