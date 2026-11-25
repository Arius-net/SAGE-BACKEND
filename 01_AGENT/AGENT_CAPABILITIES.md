# Capacidades del Agente — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`

---

## 1. Capacidades Bajo Tarea Autorizada

Cuando existe autorización explícita del responsable (`Sayd Quevedo`) o una tarea activa en `03_MEMORY/state/ACTIVE_TASK.yaml` (`authorized: true`), el agente puede:

1. **Inspección y auditoría documental:** verificar consistencia cruzada de fechas, IDs (`D-0001`, `DEC-01`, `DEC-02`, `D01`–`D06`), supuestos, sintaxis YAML/CSV y cumplimiento de reglas de gobernanza.
2. **Formulación del problema y línea base (`D01`):** estructurar modelos matemáticos/agronómicos de las 4 VD y 4 VO, diseñar escenarios piloto (3 a 10 parcelas, 10 ciclos `PV`/`OI`) y especificar el cálculo de la línea base.
3. **Evaluación arquitectónica imparcial (`D02`):** construir matrices comparativas de stack tecnológico evaluando reproducibilidad, mantenibilidad, soporte de pruebas y generación de gráficas sin sesgos previos.
4. **Diseño de datos y Algoritmos Genéticos (`D03`):** especificar contratos de `crops_catalog`, `env_params`, `parcels_input`, `chromosome` y `run_output`, definir operadores genéticos (selección, cruce, mutación, reparación/poda) y formular la función *Fitness* con penalizaciones explícitas.
5. **Implementación de la rebanada vertical `DEC-01` (`D04`):** codificar el motor evolutivo reproducible con `seed`, validadores *fail-fast*, cálculo de línea base, pruebas unitarias y generadores de gráfica de convergencia y Top-3 en el stack aprobado en `D02`.
6. **Experimentación y validación técnica (`D05`):** diseñar y ejecutar corridas controladas, registrar métricas en `03_MEMORY/experiments/EXPERIMENT_LOG.csv`, analizar sensibilidad y comprobar la diferenciación del Top-3 para `DEC-02`.
7. **Documentación y empaquetado final (`D06`):** consolidar guías reproducibles en `10_DOCUMENTATION/` y verificar cumplimiento de criterios de entrega académica.

---

## 2. Qué NO Cubre el Agente

- **Decisiones ejecutivas o de aprobación formal:** no puede autoaprobar entregables, stack ni cambios de alcance.
- **Validación agronómica de campo o encuestas:** SAGE emplea únicamente evidencia técnica sobre catálogos sintéticos; no realiza trabajo de campo ni sustituye peritaje agronómico profesional en explotaciones reales.
- **Modelado predictivo de clima o mercados:** queda fuera de las capacidades autorizadas para este proyecto (`D-0001`).
- **Gestión de infraestructura productiva externa o credenciales reales:** no administra servidores remotos, sensores IoT ni secretos reales.
