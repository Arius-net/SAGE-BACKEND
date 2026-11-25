# Registro de Herramientas y Entornos Autorizados — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Nota de stack:** El stack ejecutable permanece **abierto hasta `D02`/`D03`**; este registro gobierna únicamente categorías agnósticas de herramientas de trabajo.

---

## Tabla de Herramientas y Restricciones

| Herramienta / Entorno | Uso autorizado | Restricción |
| :--- | :--- | :--- |
| **Lector de archivos del repositorio** | Inspección de solo lectura en Fase 0, auditoría de consistencia cruzada y verificación de documentación/catálogos. | Respetar confidencialidad; nunca leer ni copiar credenciales locales fuera del repositorio. |
| **Editor de documentación y código del repositorio** | Crear o actualizar archivos dentro del alcance estrictamente autorizado en `ACTIVE_TASK.yaml` o instrucción directa de Sayd Quevedo. | Prohibido su uso durante Fase 0; prohibido sobrescribir asientos existentes de `03_MEMORY/decisions/DECISION_LOG.md`; prohibido dejar placeholders. |
| **Validadores de sintaxis estructurada (YAML / CSV / Markdown)** | Comprobar validez sintáctica de `PROJECT_STATUS.yaml`, `ACTIVE_TASK.yaml`, `config/environment.example.yaml`, `EXPERIMENT_LOG.csv` y estructura Markdown sin bloques anidados. | Solo lectura o verificación local; no modificar archivos automáticamente sin autorización. |
| **Control de versiones (Git)** | Consultar estado, diferencias e historial para trazabilidad y control SemVer; preparar cambios cuando el responsable lo autorice. | Prohibido subir `.env`, secretos, `05_DATA/raw/*` o ejecutar acciones destructivas (`force push`, reescritura de historial) sin aprobación explícita. |
| **Entorno de ejecución y pruebas (a definir en `D02`)** | Ejecutar motor del AG, pruebas unitarias (`09_VALIDATION/`), validación *fail-fast* y exportación de gráficas/tablas (`11_OUTPUTS/`) a partir de `D04`. | Bloqueado hasta la aprobación formal del stack en `D02` y del diseño en `D03`; toda corrida exige `seed` explícita y registro en `EXPERIMENT_LOG.csv`. |
| **Consultas de referencia técnica / agronómica** | Documentar parámetros sintéticos plausibles o evaluar alternativas tecnológicas objetivas en `D01`/`D02`. | Toda referencia externa debe declararse con su fuente y etiqueta epistemológica (`SUPPORTED` o `ASSUMPTION`); nunca incorporar datos personales ni feeds en tiempo real al sistema. |
