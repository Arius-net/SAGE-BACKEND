"""Motor del Algoritmo Genético de SAGE (100% determinista dada una seed)."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

import numpy as np

from .baselines import evaluate_baselines
from .evaluator import evaluate_chromosome
from .models import EvaluationResult, GAConfig, GARunResult, GenerationStats, ScenarioData


def hamming_distance(a: np.ndarray, b: np.ndarray) -> int:
    """Cuenta el número de alelos (crop_id o irrigation_level) distintos entre dos cromosomas."""
    return int(np.sum(a != b))


def initialize_population(
    scenario: ScenarioData,
    population_size: int,
    rng: np.random.Generator,
) -> List[np.ndarray]:
    """Genera población inicial reproducible dentro del dominio cerrado {0..4} x {0..4}."""
    n_parcels = len(scenario.parcels)
    n_cycles = scenario.env.total_cycles
    seasons = scenario.env.cycle_seasons

    compatible_by_season: Dict[str, List[int]] = {
        "PV": [cid for cid, c in sorted(scenario.crops.items()) if "PV" in c.compatible_seasons],
        "OI": [cid for cid, c in sorted(scenario.crops.items()) if "OI" in c.compatible_seasons],
    }

    population: List[np.ndarray] = []
    half = population_size // 2

    for idx in range(population_size):
        chrom = np.zeros((n_parcels, n_cycles, 2), dtype=np.int32)
        if idx < half:
            # Muestreo completamente uniforme en {0..4} x {0..4}
            chrom[:, :, 0] = rng.integers(0, 5, size=(n_parcels, n_cycles), dtype=np.int32)
            chrom[:, :, 1] = rng.integers(0, 5, size=(n_parcels, n_cycles), dtype=np.int32)
        else:
            # Muestreo guiado por temporada compatible con riego aleatorio en {0..4}
            for t in range(n_cycles):
                valid_crops = compatible_by_season[seasons[t]]
                chrom[:, t, 0] = rng.choice(valid_crops, size=n_parcels).astype(np.int32)
                chrom[:, t, 1] = rng.integers(0, 5, size=n_parcels, dtype=np.int32)
        population.append(chrom)
    return population


def tournament_select(
    evaluated: Sequence[EvaluationResult],
    tournament_size: int,
    rng: np.random.Generator,
) -> EvaluationResult:
    """Selección por torneo de tamaño k."""
    k = min(tournament_size, len(evaluated))
    indices = rng.choice(len(evaluated), size=k, replace=False)
    best_idx = max(indices, key=lambda i: evaluated[int(i)].fitness)
    return evaluated[int(best_idx)]


def crossover(
    parent_a: np.ndarray,
    parent_b: np.ndarray,
    crossover_rate: float,
    rng: np.random.Generator,
) -> Tuple[np.ndarray, np.ndarray]:
    """Cruce híbrido (por punto temporal por parcela o uniforme por gen) preservando dominio."""
    child_a = parent_a.copy()
    child_b = parent_b.copy()

    if rng.random() >= crossover_rate:
        return child_a, child_b

    n_parcels, n_cycles, _ = parent_a.shape
    if rng.random() < 0.5:
        # Cruce por punto temporal independiente por parcela
        for p in range(n_parcels):
            cut = int(rng.integers(1, n_cycles))
            child_a[p, cut:, :] = parent_b[p, cut:, :]
            child_b[p, cut:, :] = parent_a[p, cut:, :]
    else:
        # Cruce uniforme por gen completo (crop_id, irrigation_level)
        mask = rng.random((n_parcels, n_cycles)) < 0.5
        child_a[mask] = parent_b[mask]
        child_b[mask] = parent_a[mask]

    return child_a, child_b


def mutate(
    chromosome: np.ndarray,
    mutation_rate: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Mutación por gen estrictamente acotada al dominio {0..4} x {0..4}."""
    mutated = chromosome.copy()
    n_parcels, n_cycles, _ = mutated.shape

    for p in range(n_parcels):
        for t in range(n_cycles):
            if rng.random() < mutation_rate:
                mode = rng.random()
                if mode < 0.50:
                    current_crop = int(mutated[p, t, 0])
                    choices = [c for c in range(5) if c != current_crop]
                    mutated[p, t, 0] = int(rng.choice(choices))
                elif mode < 0.80:
                    current_irr = int(mutated[p, t, 1])
                    choices = [r for r in range(5) if r != current_irr]
                    mutated[p, t, 1] = int(rng.choice(choices))
                else:
                    mutated[p, t, 0] = int(rng.integers(0, 5))
                    mutated[p, t, 1] = int(rng.integers(0, 5))
    return mutated


def select_distinct_top_k(
    candidates: Sequence[EvaluationResult],
    k: int = 3,
    min_hamming: int = 8,
) -> List[EvaluationResult]:
    """Selecciona los k mejores individuos estructuralmente distintos (DEC-02)."""
    if not candidates:
        raise RuntimeError("No hay candidatos evaluados para seleccionar Top-K.")

    # Priorizar individuos factibles en nitrógeno y luego por Fitness descendente
    ordered = sorted(
        candidates,
        key=lambda ev: (1 if ev.is_feasible_nitrogen else 0, ev.fitness),
        reverse=True,
    )

    thresholds = sorted({min_hamming, 6, 4, 2, 1}, reverse=True)
    thresholds = [th for th in thresholds if th <= min_hamming]
    if 1 not in thresholds:
        thresholds.append(1)

    for threshold in thresholds:
        selected: List[EvaluationResult] = []
        for cand in ordered:
            if all(hamming_distance(cand.chromosome, s.chromosome) >= threshold for s in selected):
                selected.append(cand)
                if len(selected) == k:
                    return selected

    raise RuntimeError(
        f"Fallo fail-fast: la población no contiene {k} individuos estructuralmente distintos."
    )


def run_genetic_algorithm(
    scenario: ScenarioData,
    config: GAConfig,
    *,
    run_id: str = "SAGE_RUN",
) -> GARunResult:
    """Ejecuta el ciclo evolutivo completo de SAGE de forma reproducible."""
    if config.population_size < 6:
        raise ValueError("population_size debe ser >= 6.")
    if config.generations < 1:
        raise ValueError("generations debe ser >= 1.")
    if config.elitism_count < 1 or config.elitism_count >= config.population_size:
        raise ValueError("elitism_count debe estar en [1, population_size - 1].")

    rng = np.random.default_rng(config.seed)
    population = initialize_population(scenario, config.population_size, rng)

    history: List[GenerationStats] = []
    archive: Dict[bytes, EvaluationResult] = {}

    def _eval_pop(pop: List[np.ndarray]) -> List[EvaluationResult]:
        results = [
            evaluate_chromosome(
                chrom,
                scenario,
                penalty_overrides=config.penalty_overrides,
                weight_overrides=config.weight_overrides,
            )
            for chrom in pop
        ]
        results.sort(key=lambda r: r.fitness, reverse=True)
        # Guardar los mejores únicos en el archivo histórico para preservar diversidad Top-3
        for res in results[:20]:
            key = res.chromosome.tobytes()
            if key not in archive:
                archive[key] = res
        return results

    evaluated = _eval_pop(population)

    for gen in range(config.generations + 1):
        fits = [e.fitness for e in evaluated]
        feas_ratio = sum(1 for e in evaluated if e.is_feasible_nitrogen) / len(evaluated)
        history.append(
            GenerationStats(
                generation=gen,
                best_fitness=float(fits[0]),
                mean_fitness=float(np.mean(fits)),
                worst_fitness=float(fits[-1]),
                feasible_ratio=float(feas_ratio),
            )
        )

        if gen == config.generations:
            break

        # Poda + Elitismo: preservar los mejores intactos
        next_pop: List[np.ndarray] = [
            evaluated[i].chromosome.copy() for i in range(config.elitism_count)
        ]

        while len(next_pop) < config.population_size:
            p_a = tournament_select(evaluated, config.tournament_size, rng)
            p_b = tournament_select(evaluated, config.tournament_size, rng)
            c_a, c_b = crossover(p_a.chromosome, p_b.chromosome, config.crossover_rate, rng)
            c_a = mutate(c_a, config.mutation_rate, rng)
            next_pop.append(c_a)
            if len(next_pop) < config.population_size:
                c_b = mutate(c_b, config.mutation_rate, rng)
                next_pop.append(c_b)

        evaluated = _eval_pop(next_pop)

    # Asegurar que toda la población final también participa en el archivo Top-3
    for res in evaluated:
        key = res.chromosome.tobytes()
        if key not in archive:
            archive[key] = res

    top_3 = select_distinct_top_k(
        list(archive.values()),
        k=3,
        min_hamming=config.min_top3_hamming_distance,
    )
    baselines = evaluate_baselines(
        scenario,
        penalty_overrides=config.penalty_overrides,
        weight_overrides=config.weight_overrides,
    )

    return GARunResult(
        run_id=run_id,
        config=config,
        scenario_id=scenario.scenario_id,
        data_vintage=scenario.data_vintage,
        history=history,
        top_individuals=top_3,
        baselines=baselines,
    )
