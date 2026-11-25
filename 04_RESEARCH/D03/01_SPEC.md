# Especificación `D03` — Contratos de Datos, Cromosoma y Operadores Genéticos

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha:** `2026-11-23`
- **Resuelve:** `OQ-04`, `OQ-05` (base) y `OQ-06` (`02_CONTEXT/OPEN_QUESTIONS.md`)

---

## 1. Contratos de Datos y Validación *Fail-Fast* (`loader.py`)

Cualquier violación en los archivos de `05_DATA/reference/` lanza `DataValidationError` y detiene inmediatamente la ejecución:

1. **`crops_catalog.json`:**
   - Metadatos obligatorios: `schema_version`, `data_vintage` (cadena no vacía).
   - Exactamente 5 cultivos con `crop_id` igual al conjunto `{0, 1, 2, 3, 4}` (sin duplicados ni faltantes).
   - `compatible_seasons`: lista no vacía contenida en `{"PV", "OI"}`.
   - `base_cost_usd_ha >= 0`, `nominal_yield_ton_ha >= 0`, `reference_price_usd_ton >= 0`, `water_req_mm["PV"] >= 0`, `water_req_mm["OI"] >= 0`.
2. **`env_params.json`:**
   - Metadatos obligatorios: `data_vintage` no vacía.
   - `horizon`: `years == 5`, `cycles_per_year == 2`, `total_cycles == 10`, `cycle_seasons` de longitud 10 alternando `PV`/`OI`.
   - `irrigation_levels_mm`: claves exactas `{"0", "1", "2", "3", "4"}` con valores `>= 0`.
   - `fitness_weights`: claves `w_production`, `w_cost`, `w_nitrogen`, `w_water` no negativas cuya suma sea `1.0 ± 1e-6`.
   - `penalties`: valores no negativos para `nitrogen_depletion_per_violation`, `out_of_season_per_violation`, `consecutive_monoculture_per_violation`.
3. **`parcels_input.json`:**
   - Metadatos obligatorios: `data_vintage` y `scenario_id` no vacíos.
   - Número de parcelas `P` estrictamente en `[3, 10]`.
   - Cada parcela con `parcel_id` único, `area_ha > 0` y `initial_nitrogen_kg_ha > critical_min_kg_ha` (`N_0 > 0`).

---

## 2. Codificación del Cromosoma

El cromosoma se representa como un tensor entero `int32` de dimensión `(P, T, 2)`:

    Forma: (P, 10, 2)   [Para PILOT_5P_10C: (5, 10, 2) = 50 genes = 100 alelos enteros]
    Eje 0 (p): índice de parcela (0..P-1)
    Eje 1 (t): índice de ciclo   (0..9, alternando PV en pares 0,2,4,6,8 y OI en impares 1,3,5,7,9)
    Eje 2 (0): crop_id           in {0, 1, 2, 3, 4}
    Eje 2 (1): irrigation_level  in {0, 1, 2, 3, 4}

**Invariante estricto de dominio:** En todo instante (inicialización, cruce y mutación) se garantiza `0 <= crop_id <= 4` y `0 <= irrigation_level <= 4`.

---

## 3. Operadores Genéticos (Deterministas con `seed`)

Todo el proceso usa una única instancia `rng = np.random.default_rng(seed)` (`PCG64`):

1. **Inicialización poblacional (`initialize_population`):**
   - Genera `population_size` cromosomas de forma `(P, T, 2)`.
   - Para evitar arranques completamente infactibles sin sesgar la exploración, el 50% de la población inicial se muestrea uniformemente en `{0..4} × {0..4}` y el 50% restante se muestrea respetando temporadas compatibles del catálogo con riego aleatorio en `{0..4}` (`ASSUMPTION`: acelera la salida de regiones infactibles preservando diversidad genética alta).
2. **Evaluación (`evaluate_chromosome`):**
   - Calcula las 4 VO, las trayectorias exactas de nitrógeno `N_{p,t}`, el balance hídrico por ciclo, las violaciones (`V_nitrogen`, `V_season`, `V_mono`) y el puntaje escalar `Fitness`.
3. **Selección por torneo (`tournament_select`):**
   - Selecciona `k = tournament_size` individuos al azar sin sesgo y elige el de mayor `Fitness`.
4. **Cruce híbrido por parcela y ciclo (`crossover`):**
   - Con probabilidad `crossover_rate`, elige aleatoriamente entre:
     - **Cruce por punto temporal (por parcela):** para cada parcela corta en `cut in [1, T-1]` intercambiando el bloque temporal `(crop_id, irrigation_level)` completo.
     - **Cruce uniforme por gen:** intercambia genes completos `(crop_id, irrigation_level)` con probabilidad `0.5`.
   - Como ambos padres satisfacen el invariante de dominio `{0..4}`, los hijos garantizan 100% pertenencia al dominio (`RSK-03`).
5. **Mutación controlada (`mutate`):**
   - Para cada gen `(p, t)`, con probabilidad `mutation_rate`:
     - Puede mutar el `crop_id` a un valor distinto en `{0..4}` (probabilidad `0.5`), mutar `irrigation_level` a un valor distinto en `{0..4}` (probabilidad `0.3`), o ajustar ambos simultáneamente (probabilidad `0.2`).
   - Todos los valores mutados se muestrean exclusivamente dentro de `{0, 1, 2, 3, 4}`.
6. **Poda y elitismo (`elitism_count`):**
   - Se ordena la población por `Fitness` descendente, se copian intactos los `elitism_count` mejores individuos (poda de los peores reemplazada por descendencia), evitando retroceso del mejor *Fitness* histórico.

---

## 4. Selección de los 3 Mejores Individuos Distintos (`DEC-02`)

Para mitigar `RSK-01` (reportar 3 copias casi idénticas), el motor mantiene un archivo histórico de candidatos únicos evaluados a lo largo de la evolución (priorizando individuos factibles `V_nitrogen == 0`) y selecciona el Top-3 mediante selección voraz por *Fitness* descendente con filtro de **distancia estructural de Hamming mínima**:

    distancia(A, B) = número de alelos (p, t, k) donde A[p, t, k] != B[p, t, k]

- Se exige `distancia >= min_top3_hamming_distance` (por defecto `6` alelos distintos en `50` genes, `>= 6%` del cromosoma) entre cada par del Top-3.
- Si el archivo no contiene 3 individuos a esa distancia, el umbral se relaja gradualmente (`>= 4`, `>= 2`, `>= 1`) garantizando siempre 3 individuos estrictamente distintos (`distancia >= 1`) o fallando explícitamente (*fail-fast*) si la población colapsó a menos de 3 soluciones únicas.
