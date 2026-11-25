"""Pruebas de invariantes de dominio en operadores genéticos (cruce y mutación)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from sage.ga_engine import crossover, initialize_population, mutate
from sage.loader import load_scenario, validate_chromosome

DATA_REF = Path(__file__).resolve().parents[1] / "05_DATA" / "reference"


def test_crossover_and_mutation_preserve_closed_domain() -> None:
    scenario = load_scenario(DATA_REF)
    rng = np.random.default_rng(12345)
    pop = initialize_population(scenario, 30, rng)

    for chrom in pop:
        validate_chromosome(chrom, scenario)

    # Ejecutar 200 cruces y mutaciones agresivas verificando dominio {0..4} x {0..4}
    for i in range(200):
        pa = pop[i % len(pop)]
        pb = pop[(i + 7) % len(pop)]
        ca, cb = crossover(pa, pb, crossover_rate=1.0, rng=rng)
        ma = mutate(ca, mutation_rate=0.50, rng=rng)
        mb = mutate(cb, mutation_rate=0.50, rng=rng)
        validate_chromosome(ma, scenario)
        validate_chromosome(mb, scenario)
        assert ma.shape == (5, 10, 2)
        assert mb.shape == (5, 10, 2)
        assert np.all((ma >= 0) & (ma <= 4))
        assert np.all((mb >= 0) & (mb <= 4))
