# Contexto y Contrato de Datos — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Fecha de línea base:** `2026-11-23`
- **Naturaleza de los datos:** Datos sintéticos y catálogos agronómicos estáticos (`Base de Conocimiento`). Cero PII, cero PHI, cero secretos reales.
- **Stack de persistencia:** Abierto hasta `D02`/`D03` (los nombres de artefactos describen contratos lógicos, no un motor de base de datos específico).

---

## 1. Prueba de Suficiencia de Datos Estructurados y Catálogos

Para respaldar `DEC-01` y `DEC-02` sin recurrir a modelos predictivos ni fuentes externas no controladas, el conjunto mínimo suficiente de datos estructurados debe responder cuatro preguntas cuantitativas por parcela y ciclo (`PV`/`OI`):

1. **¿Cuánto cuesta y cuánto produce cada cultivo?** Cubierto por el catálogo agronómico (`crops_catalog`) para los 5 estados (`0` Barbecho/Descanso, `1` Maíz, `2` Frijol, `3` Sorgo, `4` Avena/Trigo).
2. **¿Cómo cambia el nitrógeno del suelo (`N`) tras cada ciclo?** Cubierto por los coeficientes de extracción/fijación/recuperación de `N` por cultivo en `crops_catalog` aplicados sobre el estado inicial en `parcels_input`.
3. **¿Cuál es la demanda hídrica real por cultivo y temporada (`PV`/`OI`)?** Cubierto por los perfiles de temporada y costos/límites hídricos de `env_params` cruzados con `crops_catalog`.
4. **¿Qué plan propone el AG y cómo se compara con la línea base?** Cubierto por la estructura del individuo (`chromosome`) y las salidas reproducibles con trazabilidad (`run_output`).

**Resultado de la prueba de suficiencia:** `SUPPORTED` — Los cinco artefactos lógicos definidos abajo son suficientes para cerrar `DEC-01` y `DEC-02` de punta a punta; no se requieren feeds meteorológicos en vivo, históricos de mercado ni datos personales.

---

## 2. Matriz de Responsabilidades de Artefactos de Datos

| Artefacto lógico | Rol en SAGE | Contenido mínimo esperado (definición exacta en `D03`) | Consumidor principal |
| :--- | :--- | :--- | :--- |
| `crops_catalog` | Catálogo maestro de cultivos (`Base de Conocimiento`) | Códigos `0..4`, temporadas compatibles (`PV`/`OI`), costo base por hectárea/ciclo, rendimiento nominal, precio de referencia estático, delta de nitrógeno (`ΔN`), requerimiento hídrico base y `data_vintage`. | Evaluador de *Fitness*, módulo de línea base y validadores de dominio. |
| `env_params` | Parámetros ambientales y económicos estáticos | Horizonte (`10` ciclos = `5` años), secuencia `PV`/`OI`, factores hídricos estacionales, costo unitario de agua, umbrales de penalización (`N > 0`), rango de riego factible y `data_vintage`. | Motor AG, función *Fitness* y módulo de línea base. |
| `parcels_input` | Escenario de la unidad agrícola piloto | Lista de `3` a `10` parcelas con identificador único, superficie, nivel inicial de nitrógeno (`N0 > 0`), límites hídricos locales si aplican y metadatos del escenario sintético. | Inicializador del AG, simulador de balance edáfico/hídrico y línea base. |
| `chromosome` | Representación interna de un plan candidato (`DEC-01`) | Matriz o secuencia estructurada por `(parcela, ciclo 1..10)` con alelos de tipo de cultivo (`0..4`) y nivel de riego asignado, más métricas evaluadas de las 4 VO y *Fitness* total. | Operadores genéticos (selección, cruce, mutación, reparación) y extractor Top-3. |
| `run_output` | Paquete reproducible de resultados (`DEC-01` y `DEC-02`) | Metadatos (`run_id`, `seed`, `data_vintage`, versiones de catálogos/código), serie de convergencia (mejor, promedio, peor por generación), **3 mejores individuos distintos** (calendario, evolución de `N`, balance costo/producción y balance hídrico) y comparación con línea base. | Generador de gráficas/tablas, `EXPERIMENT_LOG.csv` y usuarios finales. |

---

## 3. Fuente de Verdad, Sincronización y Manejo de Fallos Parciales (*Fail-Fast*)

| Artefacto | Fuente de verdad (a partir de `D03`/`D04`) | Replicación / Sincronización | Política ante fallos parciales (*Fail-Fast*) |
| :--- | :--- | :--- | :--- |
| `crops_catalog` | Archivo versionado en `05_DATA/processed/` | Lectura inmutable en memoria durante la corrida; su versión se copia a `run_output` y `EXPERIMENT_LOG.csv`. | **Abortar inmediatamente** si falta cualquiera de los códigos `0..4`, hay valores nulos/negativos inválidos o falta `data_vintage`. |
| `env_params` | Archivo versionado en `05_DATA/processed/` | Lectura inmutable por ejecución; sin sobrescritura automática en tiempo de corrida. | **Abortar inmediatamente** si el horizonte no coincide con 10 ciclos `PV`/`OI` o faltan umbrales críticos. |
| `parcels_input` | Escenario versionado en `05_DATA/processed/` | Referenciado por identificador y versión en cada corrida. | **Abortar inmediatamente** si el número de parcelas está fuera del rango piloto (`3..10`), existen IDs duplicados o `N0 <= 0`. |
| `chromosome` | Estado en ejecución dentro del motor AG (`08_APPLICATION/`) | Persistido solo para individuos seleccionados en `run_output` y casos de prueba en `09_VALIDATION/`. | **Abortar o reparar deterministamente** (según diseño de `D03`) ante alelos fuera de dominio; nunca evaluar en silencio genes corruptos. |
| `run_output` | Salida generada en `11_OUTPUTS/<run_id>/` | Resumen de métricas sincronizado manualmente o por script validado hacia `03_MEMORY/experiments/EXPERIMENT_LOG.csv`. | **Abortar y marcar corrida como fallida** si no se genera la gráfica de convergencia o falta cualquiera de los 3 mejores individuos y sus balances obligatorios (`RSK-04`). |

---

## 4. Contrato de Acceso, Seguridad y Privacidad

1. **Clasificación de datos:** 100% sintéticos y catálogos agronómicos públicos/académicos de referencia.
2. **Privacidad estricta:** Prohibido incorporar PII (nombres reales de agricultores, teléfonos, domicilios, RFC/CURP, coordenadas reales de predios privados) y PHI.
3. **Control de secretos:** Ningún archivo de datos o configuración versionado puede contener credenciales, claves API o tokens reales; usar `CHANGE_ME` en `.env.example`.
4. **Integridad de solo lectura en entradas:** El motor evolutivo trata `crops_catalog`, `env_params` y `parcels_input` como entradas de solo lectura; jamás las muta durante una ejecución.

---

## 5. Orden Sugerido de Incorporación

1. **`D01`:** Definir rangos agronómicos de referencia y escenarios piloto (3, 5 y 10 parcelas) a nivel conceptual y numérico para la línea base.
2. **`D03`:** Formalizar los esquemas exactos, restricciones de validación y fórmulas de balance sobre `crops_catalog`, `env_params`, `parcels_input`, `chromosome` y `run_output`.
3. **`D04`:** Crear los catálogos sintéticos versionados en `05_DATA/processed/`, implementar la validación *fail-fast* y generar los primeros `run_output` completos en `11_OUTPUTS/`.
4. **`D05`:** Ejecutar baterías de escenarios y sensibilidades registrando cada corrida en `03_MEMORY/experiments/EXPERIMENT_LOG.csv`.
