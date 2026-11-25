# Especificación de Decisiones (DSS) — SAGE

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Versión:** `1.0.0`
- **Estado:** Aprobado (Línea base `D-0001`)
- **Fecha de línea base:** `2026-11-23`
- **Autor / Responsable de aprobación:** Sayd Quevedo
- **Naturaleza del sistema:** DSS prescriptivo / optimización por Algoritmos Genéticos (no predictivo)
- **Stack tecnológico:** Abierto hasta `D02`/`D03`

---

## 1. Alcance Operativo y Naturaleza de los Datos

SAGE apoya la planificación táctica de una unidad agrícola multiparcela (piloto base: **3 a 10 parcelas**) durante un horizonte de **5 años** estructurado en **10 ciclos semestrales alternados**:
- **Primavera-Verano (PV):** ciclos impares (`C01`, `C03`, `C05`, `C07`, `C09`).
- **Otoño-Invierno (OI):** ciclos pares (`C02`, `C04`, `C06`, `C08`, `C10`).

Todos los insumos de entrada provienen de **datos sintéticos y catálogos agronómicos de referencia estáticos** (`Base de Conocimiento`) sin datos personales (PII), sin datos de salud (PHI) y sin integración a feeds en tiempo real. Cada decisión apoyada por el sistema deriva de las 4 Variables de Decisión (VD: tipo de cultivo `0..4`, ciclo `PV/OI`, riego y parcela) y las 4 Variables a Optimizar (VO: costo, producción, nitrógeno del suelo y desperdicio/estrés hídrico).

---

## 2. Catálogo de Decisiones Apoyadas

### 2.1 `DEC-01` — Planificación Espaciotemporal de Rotación y Riego *(Rebanada vertical prioritaria)*

| Atributo | Especificación |
| :--- | :--- |
| **ID y prioridad** | `DEC-01` — Prioritaria (rebanada vertical obligatoria a cerrar de punta a punta en `D04`) |
| **Decisión** | Definir qué cultivo (`0` Barbecho, `1` Maíz, `2` Frijol, `3` Sorgo, `4` Avena/Trigo) y qué régimen de riego asignar a cada parcela en cada uno de los 10 ciclos semestrales (PV/OI) a lo largo de 5 años. |
| **Cadencia** | Planificación multianual al inicio del horizonte de 5 años, con posibilidad de re-optimización bajo demanda ante cambios en catálogos o estado inicial de parcelas. |
| **Alternativas** | Espacio combinatorio de cromosomas válidos de tamaño `Parcelas × 10 ciclos`, combinando asignaciones de cultivo (`0..4`) y niveles de riego factibles sujetos a restricciones agronómicas y de temporada. |
| **Criterios de evaluación (VO)** | 1) Minimizar costo operativo total; 2) Maximizar producción total (toneladas / valor bruto); 3) Maximizar y preservar nitrógeno del suelo (`N > 0` en todo ciclo y parcela); 4) Minimizar desperdicio de agua y estrés hídrico (desviación respecto al requerimiento hídrico del cultivo en el ciclo). |
| **Costo del error asimétrico** | **Falso positivo (recomendar un plan que parece rentable pero agota el suelo `N <= 0` o induce estrés hídrico severo):** impacto **CRÍTICO**, porque degrada la capacidad productiva multianual y vuelve inviable la parcela en ciclos posteriores.<br>**Falso negativo (descartar un plan viable ligeramente más rentable por ser conservador en barbecho o agua):** impacto **MODERADO**, implica únicamente un costo de oportunidad acotado sin destruir el activo edáfico. |
| **Línea base de comparación** | Planificación empírica manual y estrategia de monocultivo continuo con riego fijo nominal por ciclo (sin optimización evolutiva ni balanceo simultáneo de nitrógeno y agua). |

### 2.2 `DEC-02` — Selección del Plan Operativo Final entre Alternativas Top-3 *(Secundaria)*

| Atributo | Especificación |
| :--- | :--- |
| **ID y prioridad** | `DEC-02` — Secundaria (validada completamente en `D05` sobre la salida de `DEC-01`) |
| **Decisión** | Seleccionar el plan operativo definitivo entre los **3 mejores individuos distintos** generados por el Algoritmo Genético, ponderando compromisos (*trade-offs*) financieros, edáficos e hídricos según el perfil de riesgo del decisor. |
| **Cadencia** | Al cierre de cada corrida o campaña de planificación (una selección por horizonte de 5 años o escenario evaluado). |
| **Alternativas** | Conjunto curado de exactamente **3 individuos distintos** de alto *Fitness* presentados con tabla comparativa, calendario parcela × ciclo, evolución de nitrógeno, balance costo/producción y balance hídrico. |
| **Criterios de evaluación** | Claridad del margen neto (producción vs. costo), margen de seguridad en nitrógeno (`min(N)` sobre `0`), eficiencia hídrica acumulada, diversidad estructural entre las 3 opciones y robustez ante las restricciones del catálogo. |
| **Costo del error asimétrico** | **Falso positivo (presentar 3 individuos prácticamente idénticos o con métricas engañosas/no comparables que induzcan a elegir un plan frágil):** impacto **ALTO**, anula el valor del DSS al ocultar compromisos reales.<br>**Falso negativo (omitir una variante ligeramente superior pero de diferencia marginal frente al Top-3 presentado):** impacto **BAJO**, siempre que las 3 alternativas sean factibles, diversas y superiores a la línea base. |
| **Línea base de comparación** | Selección de un único plan rígido sin análisis comparativo de *trade-offs* (o el plan único resultante del monocultivo/heurística manual). |

---

## 3. Decisor, Niveles de Profundidad, Incertidumbre y Trazabilidad

| Perfil | Nivel de profundidad requerido | Información clave consumida | Incertidumbre y límites visibles | Trazabilidad obligatoria |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador agrícola** | Ejecutivo / Comparativo | Resumen Top-3 (`DEC-02`), costo total, valor bruto/producción, balance hídrico global y alertas de riesgo edáfico. | Parámetros económicos estáticos (`ASM-01`); el resultado no es un pronóstico de utilidad garantizada ni contempla choques de mercado. | `run_id`, `seed`, `data_vintage`, versión de catálogos y comparación explícita frente a la línea base. |
| **Agrónomo** | Técnico / Parcela × Ciclo | Matriz completa de rotación (`DEC-01`), curva de nitrógeno por parcela y ciclo, desviación hídrica por cultivo/temporada y penalizaciones activas. | Dinámica simplificada de `N` (`ASM-02`) y demanda hídrica determinista (`ASM-03`); requiere validación profesional antes de aplicación real. | Identificador de catálogo agronómico, fórmulas de balance de `N` y agua documentadas en `D03`, pesos del *Fitness* aplicados. |
| **Evaluador académico** | Auditoría completa | Gráfica de convergencia del *Fitness* (mejor, promedio, peor), hiperparámetros del AG, registro de experimentos y pruebas automatizadas. | Naturaleza estocástica del AG acotada por semilla (`seed`) y sensibilidad a hiperparámetros/pesos del *Fitness*. | `EXPERIMENT_LOG.csv`, código versionado, `seed` exacta, `PROJECT_STATUS.yaml` y asientos de `DECISION_LOG.md`. |

---

## 4. Valor de la Información

La inversión en modelar la `Base de Conocimiento` estática y ejecutar optimización evolutiva solo se justifica si reduce incertidumbre decisional respecto a la línea base empírica:
1. **Valor sobre rotación (`DEC-01`):** cuantificar el impacto acumulado a 5 años de alternar cultivos extractivos (Maíz, Sorgo, Avena/Trigo) con fijadores de nitrógeno (Frijol) y recuperación (Barbecho), evitando colapsos de fertilidad invisibles en horizontes de un solo ciclo.
2. **Valor sobre riego (`DEC-01`):** penalizar explícitamente tanto el desperdicio de agua como el déficit hídrico por temporada (`PV`/`OI`), revelando ahorros operativos sin sacrificar rendimiento.
3. **Valor comparativo (`DEC-02`):** exponer 3 soluciones distintas en lugar de una sola respuesta "caja negra", habilitando la deliberación humana informada sobre *trade-offs*.

---

## 5. Frescura de Datos (`data_vintage`) e Implicación Técnica

| Fuente / Artefacto de datos | `data_vintage` esperada | Frecuencia de actualización | Implicación técnica obligatoria |
| :--- | :--- | :--- | :--- |
| `crops_catalog` (catálogo agronómico de cultivos `0..4`) | Fecha de versión explícita en metadatos (línea base `2026-11-23`) | Bajo control de cambios antes de cada campaña experimental (`D03`/`D05`) | Debe versionarse y registrarse en `EXPERIMENT_LOG.csv`; cualquier cambio invalida comparaciones directas con corridas previas de distinta versión. |
| `env_params` (parámetros ambientales y de temporada PV/OI) | Fecha de versión explícita en metadatos (línea base `2026-11-23`) | Estática por escenario; modificable solo en experimentos de sensibilidad controlados | Validar completitud y rangos no negativos en carga (*fail-fast*); prohibido asumir valores ocultos en código. |
| `parcels_input` (estado inicial de 3 a 10 parcelas: área, `N` inicial) | Marca de escenario / fecha de generación sintética | Por corrida o escenario de prueba | Debe declararse como entrada inmutable de cada corrida y conservarse su hash o versión junto al `run_output`. |
| `run_output` (convergencia y Top-3 individuos) | Marca temporal UTC + `seed` + versiones de entrada | Generado en cada ejecución del AG | Toda salida visual o tabular debe mostrar explícitamente `data_vintage`, `seed` y advertencia de naturaleza prescriptiva/estática. |

---

## 6. Criterios de Éxito frente a la Línea Base

Una solución producida por SAGE se considerará exitosa respecto a la línea base (monocultivo / planificación empírica manual) cuando cumpla simultáneamente:
1. **Factibilidad edáfica estricta:** `0` violaciones del umbral crítico de nitrógeno (`N > 0` en todas las parcelas y en los 10 ciclos) en los 3 mejores individuos.
2. **Mejora compuesta verificable:** el mejor individuo del AG supera el puntaje global de *Fitness* de la línea base en el escenario piloto (3 a 10 parcelas), mejorando el balance neto producción/costo sin degradar suelo ni agua.
3. **Eficiencia hídrica:** reducción medible de la desviación acumulada entre riego aplicado y requerimiento hídrico frente a la línea base de riego fijo.
4. **Convergencia observable:** la gráfica de convergencia (mejor, promedio, peor por generación) muestra progreso evolutivo consistente sin colapso inmediato ni divergencia numérica.
5. **Diversidad del Top-3 (`DEC-02`):** los 3 mejores individuos reportados son estructuralmente distintos y cada uno muestra de forma íntegra su calendario parcela × ciclo, evolución de `N`, balance costo/producción y balance hídrico.
6. **Reproducibilidad exacta:** ejecutar dos veces el motor con los mismos catálogos, parámetros y `seed` produce exactamente la misma curva de convergencia y los mismos 3 mejores individuos.

---

## 7. Supuestos Declarados

| ID | Supuesto | Estado epistemológico | Impacto si se invalida |
| :--- | :--- | :--- | :--- |
| `ASM-01` | Los precios de semillas, insumos, agua y valor por tonelada cosechada definidos en la `Base de Conocimiento` permanecen constantes durante los 10 ciclos (5 años). | `ASSUMPTION` | Alteraría la jerarquía de rentabilidad relativa entre cultivos en escenarios inflacionarios o de alta volatilidad comercial. |
| `ASM-02` | La salud del suelo relevante para rotación táctica puede modelarse adecuadamente mediante el balance discreto de nitrógeno (`N`) por ciclo con restricción crítica `N > 0`. | `ASSUMPTION` | Otros macronutrientes (P, K), pH o patógenos del suelo requerirían restricciones adicionales fuera del alcance actual. |
| `ASM-03` | Los requerimientos hídricos de cada cultivo en temporadas `PV` y `OI` son deterministas y conocidos a partir del catálogo estático sin variabilidad meteorológica estocástica. | `ASSUMPTION` | Sequías severas o lluvias atípicas exigirían re-optimizar el plan o incorporar márgenes de seguridad hídricos mayores. |
| `ASM-04` | Las parcelas (3 a 10) pueden planificarse de manera independiente dentro de la unidad agrícola, sin restricciones ocultas de capacidad compartida de maquinaria ni contagio espacial no modelado. | `ASSUMPTION` | Si existieran límites globales de presupuesto, agua total o maquinaria por ciclo, deberán formalizarse como restricciones globales en `D03`. |
