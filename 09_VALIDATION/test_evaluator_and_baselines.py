"""Pruebas del evaluador agronómico y las líneas base de SAGE."""

from __future__ import annotations

from pathlib import Path

from sage.baselines import evaluate_baselines
from sage.loader import load_scenario

DATA_REF = Path(__file__).resolve().parents[1] / "05_DATA" / "reference"


def test_monoculture_baseline_depletes_nitrogen_and_gets_penalized() -> None:
    scenario = load_scenario(DATA_REF)
    baselines = evaluate_baselines(scenario)
    mono = baselines["baseline_monoculture"]

    assert not mono.is_feasible_nitrogen
    assert mono.nitrogen_violations > 0
    assert mono.season_violations > 0
    assert mono.monoculture_violations > 0
    assert mono.min_nitrogen_any_cycle <= 0.0


def test_empirical_rotation_baseline_stays_feasible_and_beats_monoculture() -> None:
    scenario = load_scenario(DATA_REF)
    baselines = evaluate_baselines(scenario)
    mono = baselines["baseline_monoculture"]
    emp = baselines["baseline_empirical_rotation"]

    assert emp.is_feasible_nitrogen
    assert emp.nitrogen_violations == 0
    assert emp.season_violations == 0
    assert emp.monoculture_violations == 0
    assert emp.mean_water_deviation_mm > 0.0  # Riego fijo 300 mm genera desviación hídrica
    assert emp.fitness > mono.fitness
