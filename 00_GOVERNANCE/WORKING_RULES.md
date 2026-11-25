# Reglas de Trabajo y Gobernanza Operativa — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo

---

## 1. Colaboración Humano–Agente

1. **Autoridad humana última:** Sayd Quevedo es el único responsable de aprobar cambios de alcance, decisiones de gobernanza (`DECISION_LOG.md`), selección de stack tecnológico y transición de entregables (`D01`–`D06`).
2. **Fase 0 obligatoria antes de cualquier cambio:** Ningún agente puede crear, editar ni eliminar archivos sin ejecutar primero el protocolo de inspección en solo lectura (`01_AGENT/01_init.md` y `01_AGENT/protocols/phase_0_inspection.md`) y verificar autorización explícita del usuario o `03_MEMORY/state/ACTIVE_TASK.yaml` con `authorized: true`.
3. **Separación estricta de capas:**
   - `00_GOVERNANCE/`: autoridad, alcance, decisiones DSS, reglas y riesgos.
   - `01_AGENT/`: identidad, instrucciones, roles, protocolos, herramientas y prompts.
   - `02_CONTEXT/`: contexto compacto y vigente (enlaza a fuentes canónicas; no duplica).
   - `03_MEMORY/`: historial inmutable, experimentos, lecciones y estado estructurado en YAML.
   - `04_RESEARCH/`: protocolo y entregables secuenciales `D01`–`D06`.
4. **Cero suposiciones silenciosas:** Toda hipótesis, supuesto o dato faltante debe declararse explícitamente con su etiqueta epistemológica (`VERIFIED`, `SUPPORTED`, `HYPOTHESIS`, `ASSUMPTION`, `UNKNOWN` o `CONTRADICTED`).

---

## 2. Reglas de Ingeniería, Modelado y Datos

1. **Modelo antes que código:** Ninguna implementación del Algoritmo Genético ni de generación de salidas comienza antes de aprobar la formulación del problema (`D01`), la arquitectura y stack (`D02`) y el diseño de datos, cromosoma y función *Fitness* (`D03`).
2. **Stack tecnológico abierto hasta `D02`/`D03`:** Queda estrictamente prohibido asumir o justificar a posteriori lenguajes de programación, librerías evolutivas, motores de persistencia o frameworks de interfaz en documentos previos a `D02`.
3. **Rebanada vertical temprana:** Se prioriza cerrar de punta a punta `DEC-01` (carga de catálogos -> ejecución del AG -> convergencia -> Top-3 -> verificación básica) en `D04` antes de expandir funcionalidades secundarias.
4. **Reproducibilidad obligatoria con `seed`:** Todo experimento o corrida del motor evolutivo debe aceptar una semilla explícita (`seed`), registrar las versiones exactas de código y catálogos en `03_MEMORY/experiments/EXPERIMENT_LOG.csv` y producir resultados deterministas ante entradas idénticas.
5. **Manejo de fallos parciales (*fail-fast*):** Ante catálogos faltantes, esquemas inválidos, valores fuera de rango o fallo en la exportación de gráficas/tablas obligatorias, el sistema debe abortar explícitamente con mensaje diagnóstico claro; nunca completar silenciosamente valores faltantes ni reportar una corrida incompleta como exitosa.
6. **Privacidad y cero secretos:** SAGE opera únicamente con datos sintéticos y catálogos agronómicos estáticos. Se prohíbe incluir PII, PHI, claves reales, tokens o archivos `.env` en el repositorio.
7. **Evidencia técnica únicamente:** No se recolectan encuestas ni datos de trabajo de campo; toda validación descansa en evidencia técnica verificable (código, corridas con `seed`, pruebas, métricas y gráficas).

---

## 3. Control de Entregables y Calidad

### 3.1 Estados permitidos para entregables (`D01`–`D06`)

| Estado | Significado operativo |
| :--- | :--- |
| `not_started` | Entregable aún no autorizado ni iniciado. |
| `in_progress` | Entregable autorizado en `ACTIVE_TASK.yaml` y en elaboración activa. |
| `in_review` | Artefactos completos y validados por control de calidad, en espera de aprobación humana. |
| `approved` | Aprobado formalmente por Sayd Quevedo y reflejado en `PROJECT_STATUS.yaml` y `DECISION_LOG.md` si introduce decisiones estructurales. |
| `blocked` | Detenido por dependencia no resuelta, contradicción documental o falta de definición. |
| `superseded` | Reemplazado formalmente por una versión o decisión posterior sin borrar su historial. |

### 3.2 Regla de contradicción
- Si un agente detecta una contradicción entre dos documentos (por ejemplo, fechas, número de parcelas, variables VD/VO, estado de stack o entregables), **debe detener la ejecución**, etiquetar el conflicto como `CONTRADICTED`, reportarlo al responsable de aprobación y **nunca resolverlo silenciosamente** sobrescribiendo una fuente de autoridad.
- La jerarquía de resolución es: `03_MEMORY/decisions/DECISION_LOG.md` -> `00_GOVERNANCE/*` -> `04_RESEARCH/*` -> `02_CONTEXT/*`.

### 3.3 Estándar documental
- Prohibido dejar marcadores incompletos (`TODO`, textos de relleno o secciones vacías).
- Prohibido anidar bloques de código dentro de archivos Markdown; usar indentación de 4 espacios para árboles de directorios o ejemplos estructurados.
- Todos los archivos YAML y CSV deben validar sintácticamente antes de cerrar cualquier tarea.

---

## 4. Versionado Semántico (SemVer)

La documentación de gobernanza, los prompts en `01_AGENT/prompts/` y el código futuro siguen **SemVer (`MAYOR.MENOR.PARCHE`)**:
- **MAYOR (`X.0.0`):** cambios que alteran decisiones de gobernanza (`DEC-01`/`DEC-02`), variables VD/VO, contrato de datos o arquitectura aprobada. Requiere nuevo asiento en `DECISION_LOG.md`.
- **MENOR (`0.Y.0`):** adición retrocompatible de protocolos, entregables, escenarios de prueba o métricas sin romper contratos vigentes.
- **PARCHE (`0.0.Z`):** correcciones tipográficas, aclaraciones de redacción o ajustes menores sin impacto normativo ni funcional.
