# Contexto de Decisiones — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.1.0`
- **Fecha de actualización:** `2026-11-23`
- **Fuente canónica inmutable:** `03_MEMORY/decisions/DECISION_LOG.md`

---

## 1. Decisiones de Gobernanza Aprobadas

| ID | Fecha | Estado | Resumen vinculante |
| :--- | :--- | :--- | :--- |
| `D-0001` | `2026-11-23` | `aprobada` | Línea base constitucional: DSS prescriptivo por AG (no predictivo), 4 VD, 4 VO, `DEC-01` (rebanada vertical), `DEC-02` (Top-3 distintos), datos sintéticos sin PII/PHI/secretos, evidencia técnica y stack abierto hasta `D02`. |
| `D-0002` | `2026-11-23` | `aprobada` | Aprobación de `D01` y selección formal de stack (`D02`): Python 3.12 + NumPy (AG modular propio) + Pandas + Matplotlib + PyYAML + pytest + CLI reproducible, con escenario `PILOT_5P_10C` y 5 niveles discretos de riego. |
| `D-0003` | `2026-11-23` | `aprobada` | Cierre técnico de `D03`–`D06` con `11/11` pruebas en verde y adopción de `EXP-002` (`seed=2026`, `Fitness=0.7695`) como configuración calibrada de referencia para la entrega académica. |
| `D-0004` | `2026-11-23` | `aprobada` | Refactor estructural: centralización del código fuente del backend y `requirements.txt` en la carpeta raíz `BACKEND/` (retirando `08_APPLICATION/`) y actualización de `PYTHONPATH="BACKEND"`. |
| `D-0005` | `2026-11-23` | `aprobada` | Aprobación definitiva de parámetros (`OQ-01`–`OQ-08`), conversión de moneda a **MXN** (escala `20:1`), regeneración de gráficas/reportes en `11_OUTPUTS/` y cierre aprobado de `D06` (`pending_approval: false`). |

---

## 2. Restricciones Vigentes

1. **Inmutabilidad:** Prohibido editar `D-0001`–`D-0005`; cualquier cambio futuro se anexa como `D-0006`.
2. **Separación gobernanza vs. corridas:** Los planes agrícolas y métricas de experimentos permanecen en `03_MEMORY/experiments/EXPERIMENT_LOG.csv` y `11_OUTPUTS/`.
3. **Compuerta de Fase 0 restaurada:** `ACTIVE_TASK.yaml` queda en `authorized: false` hasta nueva instrucción de Sayd Quevedo.
