# Protocolo y Checklist de Control de Calidad — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Rol verificador recomendado:** `Auditor` (en modo solo lectura antes de cualquier entrega)

---

## 1. Gobernanza y Consistencia Documental

- [ ] Todas las referencias a la identidad del proyecto coinciden con **SAGE (Sistema Agrícola de Genética Evolutiva)**, autor **Sayd Quevedo** y línea base **`D-0001`** (`2026-11-23`).
- [ ] El sistema se describe de forma unívoca como **DSS prescriptivo / optimización por Algoritmos Genéticos** y **NO predictivo**.
- [ ] Coinciden en todos los documentos: 3 a 10 parcelas piloto, 5 años (10 ciclos `PV`/`OI`), 4 VD (cultivo `0..4`, fecha `PV`/`OI`, riego, parcela) y 4 VO (costo, producción, nitrógeno `N > 0`, desperdicio/estrés hídrico).
- [ ] `DEC-01` figura como rebanada vertical prioritaria y `DEC-02` como selección entre los **3 mejores individuos distintos**.
- [ ] El stack tecnológico permanece **abierto hasta `D02`/`D03`** (sin lenguajes, librerías de AG, bases de datos ni frameworks asumidos prematuramente).
- [ ] Ningún asiento histórico en `03_MEMORY/decisions/DECISION_LOG.md` fue modificado ni borrado.
- [ ] No se creó `03_MEMORY/evidence/EVIDENCE_REGISTER.csv` ni ningún artefacto de encuestas o trabajo de campo.

---

## 2. Integridad Técnica, Formato y Sintaxis

- [ ] No existen placeholders (`TODO`, `[completar aquí]`, secciones vacías ni resúmenes incompletos) en ningún archivo.
- [ ] No existen bloques de código anidados dentro de archivos Markdown (árboles y ejemplos embebidos usan indentación de 4 espacios).
- [ ] Todos los archivos YAML (`03_MEMORY/state/PROJECT_STATUS.yaml`, `03_MEMORY/state/ACTIVE_TASK.yaml`, `config/environment.example.yaml`) tienen sintaxis válida.
- [ ] Todos los archivos CSV (`03_MEMORY/experiments/EXPERIMENT_LOG.csv`) tienen encabezado intacto y sintaxis válida.
- [ ] Todas las rutas internas referenciadas existen o están declaradas explícitamente como carpetas futuras (`05_DATA/`, `08_APPLICATION/`, `09_VALIDATION/`, `10_DOCUMENTATION/`, `11_OUTPUTS/`).
- [ ] Toda afirmación relevante declara su etiqueta epistemológica (`VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN`, `CONTRADICTED`).

---

## 3. Reproducibilidad, Datos y Seguridad

- [ ] No existe ningún secreto real, credencial, archivo `.env` versionado, PII ni PHI en el repositorio (solo `CHANGE_ME` en `.env.example`).
- [ ] Para entregables con datos/código (`D03`–`D06`): existe validación *fail-fast* de `crops_catalog`, `env_params`, `parcels_input` y salidas obligatorias.
- [ ] Para entregables con ejecuciones del AG (`D04`–`D06`): cada corrida declara `seed`, `data_vintage`, registra fila completa en `EXPERIMENT_LOG.csv` y demuestra determinismo exacto al repetirse.
- [ ] Para entregables con resultados (`D04`–`D06`): se generan íntegras la gráfica de convergencia del *Fitness* (mejor, promedio, peor) y las vistas tabulares/visuales de los 3 mejores individuos distintos con comparación contra la línea base.

---

## 4. Auditoría Independiente en Solo Lectura

- [ ] Se ejecutó una revisión final de consistencia cruzada en modo solo lectura (`PROJECT_STATUS.yaml` == `CURRENT_STATE.md` == `ACTIVE_TASK.yaml` == `DECISION_LOG.md`).
- [ ] Si se detectó alguna discrepancia, se marcó como `CONTRADICTED` y se bloqueó la transición de estado hasta su resolución formal.
- [ ] El reporte final declara explícitamente qué quedó verificado, qué riesgos residuales permanecen y qué aprobación se solicita a **Sayd Quevedo**.
