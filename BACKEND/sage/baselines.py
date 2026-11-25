"""Simuladores deterministas de Línea Base para comparación justa con SAGE."""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from .evaluator import evaluate_chromosome
from .models import EvaluationResult, ScenarioData


def build_monoculture_baseline(scenario: ScenarioData) -> np.ndarray:
    """Línea Base 1: Monocultivo continuo de Maíz (crop_id=1) con riego intensivo (600 mm)."""
    n_parcels = len(scenario.parcels)
    n_cycles = scenario.env.total_cycles
    chrom = np.zeros((n_parcels, n_cycles, 2), dtype=np.int32)
    chrom[:, :, 0] = 1  # Maíz continuo
    chrom[:, :, 1] = 4  # 600 mm fijo
    return chrom


def build_empirical_rotation_baseline(scenario: ScenarioData) -> np.ndarray:
    """Línea Base 2: Rotación empírica manual con riego fijo intermedio (300 mm)."""
    n_parcels = len(scenario.parcels)
    n_cycles = scenario.env.total_cycles
    # Secuencia manual fija PV/OI: Maíz, Barbecho, Sorgo, Frijol, Maíz, Barbecho, Frijol, Avena/Trigo, Sorgo, Barbecho
    pattern = np.array([1, 0, 3, 2, 1, 0, 2, 4, 3, 0], dtype=np.int32)
    chrom = np.zeros((n_parcels, n_cycles, 2), dtype=np.int32)
    for p in range(n_parcels):
        chrom[p, :, 0] = pattern
        chrom[p, :, 1] = 2  # 300 mm fijo en todos los ciclos
    return chrom


def evaluate_baselines(
    scenario: ScenarioData,
    *,
    penalty_overrides: Optional[Dict[str, float]] = None,
    weight_overrides: Optional[Dict[str, float]] = None,
) -> Dict[str, EvaluationResult]:
    """Evalúa ambas líneas base bajo las mismas reglas de Fitness que el AG."""
    return {
        "baseline_monoculture": evaluate_chromosome(
            build_monoculture_baseline(scenario),
            scenario,
            penalty_overrides=penalty_overrides,
            weight_overrides=weight_overrides,
        ),
        "baseline_empirical_rotation": evaluate_chromosome(
            build_empirical_rotation_baseline(scenario),
            scenario,
            penalty_overrides=penalty_overrides,
            weight_overrides=weight_overrides,
        ),
    }
