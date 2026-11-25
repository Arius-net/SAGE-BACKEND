"""Modelos de datos tipados para SAGE."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np


@dataclass(frozen=True)
class Crop:
    crop_id: int
    name: str
    category: str
    compatible_seasons: tuple[str, ...]
    base_cost_mxn_ha: float
    nominal_yield_ton_ha: float
    reference_price_mxn_ton: float
    nitrogen_delta_kg_ha: float
    water_req_mm: Dict[str, float]


@dataclass(frozen=True)
class Parcel:
    parcel_id: str
    name: str
    area_ha: float
    initial_nitrogen_kg_ha: float
    soil_profile: str


@dataclass(frozen=True)
class EnvParams:
    schema_version: str
    data_vintage: str
    years: int
    cycles_per_year: int
    total_cycles: int
    cycle_seasons: tuple[str, ...]
    irrigation_levels_mm: Dict[int, float]
    water_cost_mxn_per_mm_ha: float
    currency: str
    critical_min_kg_ha: float
    target_healthy_kg_ha: float
    max_capacity_kg_ha: float
    depleted_yield_factor: float
    out_of_season_yield_factor: float
    monoculture_yield_factor: float
    min_water_stress_yield_factor: float
    fitness_weights: Dict[str, float]
    penalties: Dict[str, float]
    normalization_scales: Dict[str, float]


@dataclass(frozen=True)
class ScenarioData:
    scenario_id: str
    data_vintage: str
    crops: Dict[int, Crop]
    env: EnvParams
    parcels: tuple[Parcel, ...]


@dataclass
class EvaluationResult:
    chromosome: np.ndarray
    fitness: float
    base_score: float
    penalty_total: float
    score_production: float
    score_cost: float
    score_nitrogen: float
    score_water: float
    total_cost_mxn: float
    total_revenue_mxn: float
    net_profit_mxn: float
    total_production_ton: float
    mean_final_nitrogen: float
    min_nitrogen_any_cycle: float
    final_nitrogen_by_parcel: List[float]
    nitrogen_trajectory: np.ndarray  # shape: (P, T + 1)
    total_water_applied_mm_ha: float
    total_water_required_mm_ha: float
    mean_water_deviation_mm: float
    water_applied_by_cycle: List[float]
    water_required_by_cycle: List[float]
    nitrogen_violations: int
    season_violations: int
    monoculture_violations: int
    is_feasible_nitrogen: bool


@dataclass(frozen=True)
class GAConfig:
    population_size: int = 80
    generations: int = 120
    crossover_rate: float = 0.85
    mutation_rate: float = 0.08
    tournament_size: int = 4
    elitism_count: int = 4
    seed: int = 42
    min_top3_hamming_distance: int = 8
    penalty_overrides: Optional[Dict[str, float]] = None
    weight_overrides: Optional[Dict[str, float]] = None


@dataclass(frozen=True)
class GenerationStats:
    generation: int
    best_fitness: float
    mean_fitness: float
    worst_fitness: float
    feasible_ratio: float


@dataclass
class GARunResult:
    run_id: str
    config: GAConfig
    scenario_id: str
    data_vintage: str
    history: List[GenerationStats] = field(default_factory=list)
    top_individuals: List[EvaluationResult] = field(default_factory=list)
    baselines: Dict[str, EvaluationResult] = field(default_factory=dict)
