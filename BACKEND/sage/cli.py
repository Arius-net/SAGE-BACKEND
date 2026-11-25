"""Interfaz CLI reproducible de SAGE para corridas individuales y campaña D05."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import List

from . import __version__
from .ga_engine import run_genetic_algorithm
from .loader import load_scenario
from .models import GAConfig
from .reporting import export_run_outputs


def _cmd_run(args: argparse.Namespace) -> int:
    scenario = load_scenario(args.data_dir)
    config = GAConfig(
        population_size=args.pop_size,
        generations=args.generations,
        crossover_rate=args.crossover_rate,
        mutation_rate=args.mutation_rate,
        tournament_size=args.tournament_size,
        elitism_count=args.elitism_count,
        seed=args.seed,
        min_top3_hamming_distance=args.min_hamming,
    )
    run = run_genetic_algorithm(scenario, config, run_id=args.run_id)
    paths = export_run_outputs(run, scenario, args.output_dir)

    best = run.top_individuals[0]
    emp = run.baselines["baseline_empirical_rotation"]
    print(
        f"[SAGE {run.run_id}] Fitness Top-1={best.fitness:.4f} vs LB Empírica={emp.fitness:.4f} | "
        f"Utilidad Neta={best.net_profit_mxn:,.2f} {scenario.env.currency} | N final prom={best.mean_final_nitrogen:.2f} kg/ha | "
        f"Desvío hídrico={best.mean_water_deviation_mm:.2f} mm | Salidas={len(paths)} archivos en {args.output_dir}"
    )
    return 0


def _cmd_campaign(args: argparse.Namespace) -> int:
    """Ejecuta la campaña experimental calibrada de D05 (3 experimentos distintos) y exporta el mejor."""
    scenario = load_scenario(args.data_dir)
    experiments: List[tuple[str, str, GAConfig]] = [
        (
            "EXP-001",
            "Línea base evolutiva: población moderada y mutación estándar (8%) con penalizaciones base",
            GAConfig(
                population_size=80,
                generations=140,
                crossover_rate=0.85,
                mutation_rate=0.08,
                tournament_size=4,
                elitism_count=4,
                seed=42,
                min_top3_hamming_distance=8,
            ),
        ),
        (
            "EXP-002",
            "Mayor exploración: población ampliada (140), 180 generaciones y mutación baja-moderada (5%) con penalización estricta de N",
            GAConfig(
                population_size=140,
                generations=180,
                crossover_rate=0.88,
                mutation_rate=0.05,
                tournament_size=5,
                elitism_count=6,
                seed=2026,
                min_top3_hamming_distance=10,
                penalty_overrides={
                    "nitrogen_depletion_per_violation": 3.50,
                    "out_of_season_per_violation": 1.10,
                    "consecutive_monoculture_per_violation": 0.85,
                },
            ),
        ),
        (
            "EXP-003",
            "Alta mutación (14%) con población media (100) y penalización moderada para evaluar estabilidad",
            GAConfig(
                population_size=100,
                generations=160,
                crossover_rate=0.80,
                mutation_rate=0.14,
                tournament_size=3,
                elitism_count=4,
                seed=777,
                min_top3_hamming_distance=8,
                penalty_overrides={
                    "nitrogen_depletion_per_violation": 2.00,
                    "out_of_season_per_violation": 0.70,
                    "consecutive_monoculture_per_violation": 0.50,
                },
            ),
        ),
    ]

    out_root = Path(args.output_dir)
    exp_dir_root = out_root / "experiments"
    exp_dir_root.mkdir(parents=True, exist_ok=True)

    runs = []
    log_rows = []
    for exp_id, objective, cfg in experiments:
        run = run_genetic_algorithm(scenario, cfg, run_id=exp_id)
        exp_out = exp_dir_root / exp_id
        export_run_outputs(run, scenario, exp_out)
        runs.append((exp_id, run))

        best = run.top_individuals[0]
        emp = run.baselines["baseline_empirical_rotation"]
        params_str = (
            f"seed={cfg.seed};pop={cfg.population_size};gen={cfg.generations};"
            f"cx={cfg.crossover_rate};mut={cfg.mutation_rate};tourn={cfg.tournament_size};"
            f"elitism={cfg.elitism_count};penalties={cfg.penalty_overrides or 'default'}"
        )
        metrics_str = (
            f"best_fitness={best.fitness:.4f};lb_emp_fitness={emp.fitness:.4f};"
            f"net_profit_mxn={best.net_profit_mxn:.2f};cost_mxn={best.total_cost_mxn:.2f};"
            f"prod_ton={best.total_production_ton:.2f};mean_final_N={best.mean_final_nitrogen:.2f};"
            f"min_N={best.min_nitrogen_any_cycle:.2f};water_dev_mm={best.mean_water_deviation_mm:.2f};"
            f"viol_N={best.nitrogen_violations};viol_temp={best.season_violations};viol_mono={best.monoculture_violations}"
        )
        log_rows.append(
            {
                "experiment_id": exp_id,
                "date": scenario.data_vintage,
                "objective": objective,
                "dataset_version": f"{scenario.scenario_id}@{scenario.data_vintage}",
                "code_version": f"sage-{__version__}",
                "method": "GeneticAlgorithm_PCG64_Tournament_HybridCrossover",
                "parameters": params_str,
                "validation_method": "Compare_vs_2_Baselines+Feasibility_N>0+SeedDeterminism",
                "metrics": metrics_str,
                "result_path": f"11_OUTPUTS/experiments/{exp_id}/",
                "status": "completed_feasible" if best.is_feasible_nitrogen else "completed_infeasible",
                "limitations": "Parametros estaticos ASM-01; balance discreto de N ASM-02; demanda hidrica determinista ASM-03",
            }
        )

    # Elegir el mejor experimento (factible y mayor Fitness Top-1) y exportar en la raíz de 11_OUTPUTS/
    best_exp_id, best_run = max(
        runs,
        key=lambda item: (1 if item[1].top_individuals[0].is_feasible_nitrogen else 0, item[1].top_individuals[0].fitness),
    )
    export_run_outputs(best_run, scenario, out_root)

    # Escribir registro limpio de experimentos en EXPERIMENT_LOG.csv
    if args.experiment_log:
        log_path = Path(args.experiment_log)
        fieldnames = [
            "experiment_id",
            "date",
            "objective",
            "dataset_version",
            "code_version",
            "method",
            "parameters",
            "validation_method",
            "metrics",
            "result_path",
            "status",
            "limitations",
        ]
        with log_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(log_rows)

    summary = {
        "best_experiment_id": best_exp_id,
        "currency": scenario.env.currency,
        "experiments": [
            {
                "experiment_id": eid,
                "seed": r.config.seed,
                "best_fitness": round(r.top_individuals[0].fitness, 6),
                "net_profit_mxn": round(r.top_individuals[0].net_profit_mxn, 2),
                "mean_final_nitrogen": round(r.top_individuals[0].mean_final_nitrogen, 2),
                "mean_water_deviation_mm": round(r.top_individuals[0].mean_water_deviation_mm, 2),
                "feasible_nitrogen": r.top_individuals[0].is_feasible_nitrogen,
            }
            for eid, r in runs
        ],
    }
    (out_root / "campaign_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sage", description="CLI de SAGE (Sistema Agrícola de Genética Evolutiva)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="Ejecuta una corrida reproducible del AG de SAGE.")
    p_run.add_argument("--data-dir", default="05_DATA/reference", help="Directorio de la Base de Conocimiento JSON.")
    p_run.add_argument("--output-dir", default="11_OUTPUTS", help="Directorio de exportación de salidas.")
    p_run.add_argument("--run-id", default="SAGE_CLI_RUN", help="Identificador de la corrida.")
    p_run.add_argument("--seed", type=int, default=42, help="Semilla pseudoaleatoria reproducible.")
    p_run.add_argument("--pop-size", type=int, default=120, help="Tamaño de población.")
    p_run.add_argument("--generations", type=int, default=160, help="Número de generaciones.")
    p_run.add_argument("--crossover-rate", type=float, default=0.85, help="Probabilidad de cruce.")
    p_run.add_argument("--mutation-rate", type=float, default=0.06, help="Probabilidad de mutación por gen.")
    p_run.add_argument("--tournament-size", type=int, default=4, help="Tamaño del torneo.")
    p_run.add_argument("--elitism-count", type=int, default=4, help="Número de individuos élite.")
    p_run.add_argument("--min-hamming", type=int, default=8, help="Distancia de Hamming mínima entre Top-3.")
    p_run.set_defaults(func=_cmd_run)

    p_camp = sub.add_parser("campaign", help="Ejecuta la campaña experimental D05 (EXP-001..EXP-003).")
    p_camp.add_argument("--data-dir", default="05_DATA/reference", help="Directorio de la Base de Conocimiento JSON.")
    p_camp.add_argument("--output-dir", default="11_OUTPUTS", help="Directorio raíz de salidas.")
    p_camp.add_argument(
        "--experiment-log",
        default="03_MEMORY/experiments/EXPERIMENT_LOG.csv",
        help="Ruta del archivo EXPERIMENT_LOG.csv a actualizar.",
    )
    p_camp.set_defaults(func=_cmd_campaign)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
