# Protocolo de Investigación y Entregables (`D01`–`D06`) — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Responsable de aprobación:** Sayd Quevedo
- **Referencia vinculante:** `03_MEMORY/decisions/DECISION_LOG.md` (`D-0001`)

---

## 1. Hoja de Ruta Secuencial `D01`–`D06`

Cada entregable representa una compuerta formal de avance. Ningún entregable puede iniciarse sin completar los prerrequisitos del anterior y contar con autorización explícita (`ACTIVE_TASK.yaml` con `authorized: true`).

| ID | Entregable | Objetivo principal en SAGE | Decisiones / Salidas clave | Prerrequisito |
| :--- | :--- | :--- | :--- | :--- |
| `D01` | **Formulación del Problema y Línea Base** | Formalizar el modelo matemático/agronómico de las 4 VD y 4 VO, definir escenarios piloto (3 a 10 parcelas, 10 ciclos `PV`/`OI`) y cuantificar la línea base (monocultivo y planificación empírica manual). | Definición formal del problema, métricas de línea base y criterios cuantitativos de comparación para `DEC-01`. | `D-0001` + autorización `D-0002` |
| `D02` | **Arquitectura del Sistema y Matriz de Stack Tecnológico** | Diseñar la arquitectura modular de SAGE y evaluar de manera objetiva opciones de lenguaje, librerías de AG, formato de catálogos y generación de gráficas/reportes sin justificaciones a posteriori. | Matriz comparativa de stack, propuesta de arquitectura y aprobación formal de tecnología (nuevo asiento en `DECISION_LOG.md`). | `D01` aprobado |
| `D03` | **Diseño de Datos, Modelo de Cromosoma y Función Fitness** | Especificar esquemas exactos de `crops_catalog`, `env_params`, `parcels_input` y `run_output`; diseñar la codificación del cromosoma, operadores genéticos (cruce, mutación, selección, reparación), normalización de las 4 VO y penalizaciones por `N <= 0` y desvío hídrico. | Contratos de datos versionados, diseño del cromosoma, fórmulas de *Fitness* y diseño de pruebas unitarias de invariantes. | `D02` aprobado |
| `D04` | **Implementación de la Rebanada Vertical `DEC-01`** | Construir de punta a punta la rebanada vertical mínima funcional en `05_DATA/`, `08_APPLICATION/`, `09_VALIDATION/` y `11_OUTPUTS/`: validación *fail-fast*, ejecución reproducible con `seed`, gráfica de convergencia y generación de los 3 mejores individuos distintos. | Motor operativo end-to-end para `DEC-01`, suite inicial de pruebas unitarias/reproducibilidad y primera corrida registrada en `EXPERIMENT_LOG.csv`. | `D03` aprobado |
| `D05` | **Calibración, Experimentación Reproducible y Validación `DEC-02`** | Ejecutar campañas experimentales controladas con múltiples `seed`, calibrar hiperparámetros y pesos del *Fitness*, comprobar superación de la línea base y validar las vistas comparativas de *trade-offs* del Top-3 para `DEC-02`. | Matriz de experimentos en `EXPERIMENT_LOG.csv`, análisis de sensibilidad, evidencia de convergencia y validación integral de `DEC-01` y `DEC-02`. | `D04` aprobado |
| `D06` | **Documentación Final, Empaquetado y Defensa Académica** | Consolidar manual técnico y de usuario en `10_DOCUMENTATION/`, verificar reproducibilidad limpia de extremo a extremo, auditar trazabilidad y preparar el paquete de entrega y exposición para *Fundamentos de Inteligencia Artificial*. | Informe final, guía de ejecución reproducible, auditoría documental limpia y material de defensa académica. | `D05` aprobado |

---

## 2. Estructura Estándar por Carpeta de Entregable

Cuando se autorice cada entregable (`D01` a `D06`), se creará su carpeta bajo `04_RESEARCH/` con la siguiente estructura mínima uniforme:

    04_RESEARCH/
    └── D0X_<nombre_corto>/
        ├── README.md            # Resumen ejecutivo, alcance, estado y trazabilidad
        ├── 01_SPEC.md           # Especificación técnica o análisis principal del entregable
        ├── 02_VERIFICATION.md   # Evidencia técnica, chequeo de criterios y etiquetas epistemológicas
        └── artifacts/           # Tablas, diagramas o salidas de soporte del entregable (si aplica)

---

## 3. Estados Permitidos

Los estados oficiales de `D01`–`D06` en `03_MEMORY/state/PROJECT_STATUS.yaml` son:
- `not_started`: no autorizado ni iniciado.
- `in_progress`: autorizado en `ACTIVE_TASK.yaml` y en ejecución.
- `in_review`: completado y validado con `01_AGENT/protocols/quality_control.md`, pendiente de revisión de Sayd Quevedo.
- `approved`: aprobado formalmente por el responsable del proyecto.
- `blocked`: detenido por una dependencia externa, falta de definición o contradicción (`CONTRADICTED`).
- `superseded`: reemplazado formalmente por una revisión posterior conservando trazabilidad.

---

## 4. Criterio de Avance por Rebanada Vertical

1. **Prioridad absoluta a `DEC-01`:** Desde `D01` hasta `D04`, toda decisión de modelado, arquitectura y código debe converger en cerrar una ejecución completa y reproducible de `DEC-01` antes de agregar refinamientos visuales o análisis avanzados.
2. **Validación antes de escalar:** `D05` solo puede iniciar cuando `D04` demuestre determinismo por `seed`, cero violaciones silenciosas (*fail-fast*) y generación íntegra de la gráfica de convergencia y del Top-3.
3. **Evidencia técnica verificable:** Ningún entregable pasa a `in_review` con marcadores incompletos, datos inventados o afirmaciones sin etiqueta epistemológica.
