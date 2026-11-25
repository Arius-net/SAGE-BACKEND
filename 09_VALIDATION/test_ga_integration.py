"""Pruebas de integración: determinismo por seed, superación de línea base, N > 0 y exportación."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from sage.ga_engine import hamming_distance, run_genetic_algorithm
from sage.loader import load_scenario
from sage.models import GAConfig
from sage.reporting import export_run_outputs

DATA_REF = Path(__file__).resolve().parents[1] / "05_DATA" / "reference"


def test_exact_seed_determinism() -> None:
    scenario = load_scenario(DATA_REF)
    cfg = GAConfig(population_size=40, generations=35, seed=99, mutation_rate=0.07)

    run_a = run_genetic_algorithm(scenario, cfg, run_id="DET_A")
    run_b = run_genetic_algorithm(scenario, cfg, run_id="DET_B")

    assert [s.best_fitness for s in run_a.history] == [s.best_fitness for s in run_b.history]
    assert [s.mean_fitness for s in run_a.history] == [s.mean_fitness for s in run_b.history]
    for ind_a, ind_b in zip(run_a.top_individuals, run_b.top_individuals):
        assert np.array_equal(ind_a.chromosome, ind_b.chromosome)
        assert ind_a.fitness == ind_b.fitness


def test_sage_beats_baselines_keeps_nitrogen_positive_and_exports_outputs(tmp_path: Path) -> None:
    scenario = load_scenario(DATA_REF)
    cfg = GAConfig(population_size=80, generations=100, seed=42, mutation_rate=0.06)

    run = run_genetic_algorithm(scenario, cfg, run_id="TEST_INT")
    best = run.top_individuals[0]
    mono = run.baselines["baseline_monoculture"]
    emp = run.baselines["baseline_empirical_rotation"]

    # Superación de ambas líneas base y factibilidad estricta N > 0 en 100% de parcelas
    assert best.fitness > mono.fitness
    assert best.fitness > emp.fitness
    assert best.is_feasible_nitrogen
    assert best.nitrogen_violations == 0
    assert all(n > 0.0 for n in best.final_nitrogen_by_parcel)
    assert best.min_nitrogen_any_cycle > 0.0

    # Top-3 estructuralmente distintos
    assert len(run.top_individuals) == 3
    assert hamming_distance(run.top_individuals[0].chromosome, run.top_individuals[1].chromosome) >= 1
    assert hamming_distance(run.top_individuals[0].chromosome, run.top_individuals[2].chromosome) >= 1
    assert hamming_distance(run.top_individuals[1].chromosome, run.top_individuals[2].chromosome) >= 1

    # Exportación fail-fast completa de gráficas y tablas
    paths = export_run_outputs(run, scenario, tmp_path / "outputs")
    assert len(paths) == 8
    for p in paths.values():
        assert p.exists() and p.stat().st_size > 0
