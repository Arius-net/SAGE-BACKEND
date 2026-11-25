# Especificación `D01` — Formulación Matemática, Escenario Piloto y Línea Base

- **Proyecto:** SAGE (*Sistema Agrícola de Genética Evolutiva*)
- **Fecha de línea base:** `2026-11-23`
- **Decisión prioritaria:** `DEC-01` (rebanada vertical) y soporte a `DEC-02` (Top-3 distintos)
- **Estado epistemológico:** `SUPPORTED` (parámetros sintéticos plausibles marcados como `ASSUMPTION` donde requieren calibración humana final)

---

## 1. Escenario Piloto Sintético (`PILOT_5P_10C`)

Se construyó el escenario de referencia en `05_DATA/reference/` con `data_vintage = "2026-11-23"`, cero PII, cero PHI y cero secretos:

- **Parcelas (`parcels_input.json`):** `P = 5` parcelas heterogéneas (`P1` a `P5`) con superficies entre `2.5` y `5.0 ha` (total `18.0 ha`) y nitrógeno inicial `N_0` entre `40.0` y `64.0 kg/ha`.
- **Horizonte (`env_params.json`):** `T = 10` ciclos semestrales (5 años) alternados `PV` (ciclos impares `1, 3, 5, 7, 9`) y `OI` (ciclos pares `2, 4, 6, 8, 10`).
- **Catálogo de cultivos (`crops_catalog.json`):**

| `crop_id` | Cultivo | Temporadas compatibles | Costo base (`USD/ha`) | Rendimiento nominal (`ton/ha`) | Precio ref. (`USD/ton`) | `ΔN` (`kg/ha`) | Demanda hídrica `PV` / `OI` (`mm`) |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: | :---: |
| `0` | Barbecho/Descanso | `PV`, `OI` | 80 | 0.0 | 0 | +26.0 | 0 / 0 |
| `1` | Maíz | `PV` | 620 | 9.5 | 230 | -32.0 | 600 / 450 |
| `2` | Frijol | `PV`, `OI` | 440 | 2.4 | 780 | +24.0 | 300 / 150 |
| `3` | Sorgo | `PV` | 410 | 6.8 | 195 | -20.0 | 450 / 300 |
| `4` | Avena/Trigo | `OI` | 390 | 5.6 | 250 | -18.0 | 450 / 300 |

- **Niveles discretos de riego (`irrigation_levels_mm`):** `0 -> 0 mm`, `1 -> 150 mm`, `2 -> 300 mm`, `3 -> 450 mm`, `4 -> 600 mm`. Costo unitario del agua: `0.45 USD/(mm·ha)` (`ASSUMPTION`).

---

## 2. Variables de Decisión (VD)

Para cada parcela `p in {1..P}` y cada ciclo `t in {1..T}` (con temporada `s(t) in {PV, OI}`), el gen `g_{p,t}` define:

    g_{p,t} = (c_{p,t}, r_{p,t})
    donde:
      c_{p,t} in {0, 1, 2, 3, 4}   (Tipo de cultivo)
      r_{p,t} in {0, 1, 2, 3, 4}   (Nivel de riego asignado -> W_{p,t} in {0, 150, 300, 450, 600} mm)

---

## 3. Dinámica Agronómica y Económica por Parcela y Ciclo

Para cada parcela `p` (área `A_p` en hectáreas) y ciclo `t`:

1. **Factor de estrés hídrico (`f_water`):**
   - Si demanda hídrica `W_req(c_{p,t}, s(t)) == 0`: `f_water = 1.0`.
   - Si `W_req > 0`: `f_water = min(1.0, max(0.25, W_{p,t} / W_req))`.
   - Desviación hídrica absoluta (desperdicio + déficit): `D_water(p, t) = |W_{p,t} - W_req(c_{p,t}, s(t))|`.
2. **Factor de temporada (`f_season`):**
   - `1.0` si `s(t)` está en `compatible_seasons(c_{p,t})`, de lo contrario `0.35` y suma 1 violación `v_season`.
3. **Factor de monocultivo consecutivo (`f_mono`):**
   - Si `t > 1`, `c_{p,t} == c_{p,t-1}` y `c_{p,t} != 0`: `f_mono = 0.80` y suma 1 violación `v_mono`; en otro caso `1.0`.
4. **Actualización de nitrógeno del suelo (`N_{p,t}`) y factor edáfico (`f_soil`):**
   - Antes de cosechar, se evalúa la suficiencia del suelo: `N_post = N_{p,t-1} + ΔN(c_{p,t})`.
   - Si `N_{p,t-1} <= 0` o `N_post <= 0`: `f_soil = 0.20` y suma 1 violación crítica `v_nitrogen` (violación de `N > 0`, cubriendo estrictamente `N <= 0` y `N < 0`).
   - El estado edáfico para el siguiente ciclo se actualiza con tope de capacidad: `N_{p,t} = min(N_max, N_post)`, donde `N_max = 120.0 kg/ha`.
5. **Producción y valor bruto (`VO-2`):**
   - `Y_{p,t} = A_p * yield_nom(c_{p,t}) * f_water * f_season * f_mono * f_soil` (toneladas).
   - `Rev_{p,t} = Y_{p,t} * price(c_{p,t})` (USD).
6. **Costo operativo total (`VO-1`):**
   - `Cost_{p,t} = A_p * (base_cost(c_{p,t}) + water_cost_per_mm_ha * W_{p,t})` (USD).

---

## 4. Función Fitness Multiobjetivo con Penalizaciones Explícitas

Las 4 Variables a Optimizar se consolidan mediante escalado normalizado al rango `[0, 1]` sobre la superficie total `A_total = sum(A_p)` y los `T = 10` ciclos:

    S_prod  = Total_Revenue / (A_total * T * 2200.0)                 [Maximizar]
    S_cost  = 1.0 - min(1.0, Total_Cost / (A_total * T * 950.0))     [Minimizar Costo -> Maximizar S_cost]
    S_nitro = mean_{p,t}( clamp(N_{p,t} / 45.0, 0.0, 1.0) )          [Preservar y Maximizar Nutrientes]
    S_water = 1.0 - min(1.0, mean_{p,t}(D_water(p,t)) / 600.0)       [Minimizar Desperdicio/Estrés -> Maximizar S_water]

Puntaje base ponderado (`w_prod=0.38`, `w_cost=0.22`, `w_nitro=0.22`, `w_water=0.18`; suman `1.00`):

    Base_Score = 0.38 * S_prod + 0.22 * S_cost + 0.22 * S_nitro + 0.18 * S_water

Penalización total explícita normalizada por el tamaño del cromosoma (`P * T`):

    Penalty = (2.50 * V_nitrogen + 0.85 * V_season + 0.65 * V_mono) / (P * T)
    Fitness = Base_Score - Penalty

Además, cualquier individuo con `V_nitrogen > 0` recibe una penalización adicional fija de infactibilidad (`-0.50`) para garantizar separación estricta entre soluciones sostenibles (`N > 0` en todas las parcelas y ciclos) y soluciones destructivas (`RSK-02`, costo del error asimétrico de `DECISION_SPEC.md`).

---

## 5. Definición de Líneas Base de Comparación

Para contrastar de forma justa el rendimiento de SAGE (`DEC-01`) se definen dos líneas base deterministas en el mismo escenario `PILOT_5P_10C`:

1. **Línea Base 1 — Monocultivo continuo de Maíz (`baseline_monoculture`):**
   - Todas las parcelas siembran `c = 1` (Maíz) en los 10 ciclos con riego fijo intensivo `r = 4` (`600 mm`). Representa la práctica miope de maximización a corto plazo sin rotación.
2. **Línea Base 2 — Rotación empírica manual con riego fijo (`baseline_empirical_rotation`):**
   - Todas las parcelas aplican una secuencia manual prudente pero rígida: `[Maíz(PV), Barbecho(OI), Sorgo(PV), Frijol(OI), Maíz(PV), Barbecho(OI), Frijol(PV), Avena/Trigo(OI), Sorgo(PV), Barbecho(OI)]` con riego fijo intermedio `r = 2` (`300 mm`) en todos los ciclos. Mantiene el suelo con `N > 0`, pero sufre desperdicio en Barbecho y déficit hídrico en Maíz/Sorgo.
