"""Evaluador agronómico, económico y función Fitness de SAGE."""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from .loader import validate_chromosome
from .models import EvaluationResult, ScenarioData


def evaluate_chromosome(
    chromosome: np.ndarray,
    scenario: ScenarioData,
    *,
    penalty_overrides: Optional[Dict[str, float]] = None,
    weight_overrides: Optional[Dict[str, float]] = None,
) -> EvaluationResult:
    """Simula los 10 ciclos PV/OI y calcula las 4 VO, penalizaciones y Fitness."""
    validate_chromosome(chromosome, scenario)

    env = scenario.env
    n_parcels = len(scenario.parcels)
    n_cycles = env.total_cycles

    weights = dict(env.fitness_weights)
    if weight_overrides:
        weights.update(weight_overrides)

    penalties = dict(env.penalties)
    if penalty_overrides:
        penalties.update(penalty_overrides)

    nitrogen_traj = np.zeros((n_parcels, n_cycles + 1), dtype=np.float64)
    water_applied_by_cycle = np.zeros(n_cycles, dtype=np.float64)
    water_required_by_cycle = np.zeros(n_cycles, dtype=np.float64)

    total_cost = 0.0
    total_revenue = 0.0
    total_production = 0.0
    total_water_applied_mm_ha = 0.0
    total_water_required_mm_ha = 0.0
    water_deviations_mm: list[float] = []

    nitrogen_violations = 0
    season_violations = 0
    monoculture_violations = 0

    total_area = sum(p.area_ha for p in scenario.parcels)

    for p_idx, parcel in enumerate(scenario.parcels):
        n_curr = parcel.initial_nitrogen_kg_ha
        nitrogen_traj[p_idx, 0] = n_curr
        prev_crop_id: Optional[int] = None

        for t in range(n_cycles):
            crop_id = int(chromosome[p_idx, t, 0])
            irr_lvl = int(chromosome[p_idx, t, 1])
            crop = scenario.crops[crop_id]
            season = env.cycle_seasons[t]

            w_app = env.irrigation_levels_mm[irr_lvl]
            w_req = crop.water_req_mm[season]
            w_dev = abs(w_app - w_req)
            water_deviations_mm.append(w_dev)

            water_applied_by_cycle[t] += w_app * parcel.area_ha
            water_required_by_cycle[t] += w_req * parcel.area_ha
            total_water_applied_mm_ha += w_app * parcel.area_ha
            total_water_required_mm_ha += w_req * parcel.area_ha

            if w_req <= 0.0:
                f_water = 1.0
            else:
                f_water = min(1.0, max(env.min_water_stress_yield_factor, w_app / w_req))

            if season in crop.compatible_seasons:
                f_season = 1.0
            else:
                f_season = env.out_of_season_yield_factor
                season_violations += 1

            if prev_crop_id is not None and crop_id != 0 and crop_id == prev_crop_id:
                f_mono = env.monoculture_yield_factor
                monoculture_violations += 1
            else:
                f_mono = 1.0

            n_post = n_curr + crop.nitrogen_delta_kg_ha
            if n_curr <= env.critical_min_kg_ha or n_post <= env.critical_min_kg_ha:
                f_soil = env.depleted_yield_factor
                nitrogen_violations += 1
            else:
                f_soil = 1.0

            n_next = min(env.max_capacity_kg_ha, n_post)
            nitrogen_traj[p_idx, t + 1] = n_next
            n_curr = n_next
            prev_crop_id = crop_id

            yield_ton = (
                parcel.area_ha
                * crop.nominal_yield_ton_ha
                * f_water
                * f_season
                * f_mono
                * f_soil
            )
            rev = yield_ton * crop.reference_price_mxn_ton
            cost = parcel.area_ha * (
                crop.base_cost_mxn_ha + env.water_cost_mxn_per_mm_ha * w_app
            )

            total_production += yield_ton
            total_revenue += rev
            total_cost += cost

    scales = env.normalization_scales
    s_prod = total_revenue / (total_area * n_cycles * scales["max_expected_revenue_per_ha_cycle"])
    s_cost = 1.0 - min(1.0, total_cost / (total_area * n_cycles * scales["max_expected_cost_per_ha_cycle"]))
    n_post_cycles = nitrogen_traj[:, 1:]
    s_nitro = float(np.mean(np.clip(n_post_cycles / env.target_healthy_kg_ha, 0.0, 1.0)))
    mean_water_dev = float(np.mean(water_deviations_mm))
    s_water = 1.0 - min(1.0, mean_water_dev / scales["max_expected_water_dev_mm_cycle"])

    base_score = (
        weights["w_production"] * s_prod
        + weights["w_cost"] * s_cost
        + weights["w_nitrogen"] * s_nitro
        + weights["w_water"] * s_water
    )

    total_genes = n_parcels * n_cycles
    infeasibility_penalty = 0.50 if nitrogen_violations > 0 else 0.0
    penalty_total = (
        penalties["nitrogen_depletion_per_violation"] * nitrogen_violations
        + penalties["out_of_season_per_violation"] * season_violations
        + penalties["consecutive_monoculture_per_violation"] * monoculture_violations
    ) / total_genes + infeasibility_penalty

    fitness = float(base_score - penalty_total)
    final_n_list = [float(nitrogen_traj[p, -1]) for p in range(n_parcels)]
    min_n_any = float(np.min(n_post_cycles))
    is_feasible = (nitrogen_violations == 0) and all(v > env.critical_min_kg_ha for v in final_n_list)

    return EvaluationResult(
        chromosome=chromosome.copy(),
        fitness=fitness,
        base_score=float(base_score),
        penalty_total=float(penalty_total),
        score_production=float(s_prod),
        score_cost=float(s_cost),
        score_nitrogen=float(s_nitro),
        score_water=float(s_water),
        total_cost_mxn=float(total_cost),
        total_revenue_mxn=float(total_revenue),
        net_profit_mxn=float(total_revenue - total_cost),
        total_production_ton=float(total_production),
        mean_final_nitrogen=float(np.mean(final_n_list)),
        min_nitrogen_any_cycle=min_n_any,
        final_nitrogen_by_parcel=final_n_list,
        nitrogen_trajectory=nitrogen_traj,
        total_water_applied_mm_ha=float(total_water_applied_mm_ha),
        total_water_required_mm_ha=float(total_water_required_mm_ha),
        mean_water_deviation_mm=mean_water_dev,
        water_applied_by_cycle=[float(x / total_area) for x in water_applied_by_cycle],
        water_required_by_cycle=[float(x / total_area) for x in water_required_by_cycle],
        nitrogen_violations=nitrogen_violations,
        season_violations=season_violations,
        monoculture_violations=monoculture_violations,
        is_feasible_nitrogen=is_feasible,
    )
