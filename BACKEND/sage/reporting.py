"""Exportación fail-fast de gráficas y reportes tabulares para DEC-01 y DEC-02."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .ga_engine import hamming_distance
from .models import EvaluationResult, GARunResult, ScenarioData

PRESCRIPTIVE_NOTICE = (
    "AVISO PRESCRIPTIVO (DSS): SAGE optimiza rotación de cultivos y riego sobre catálogos "
    "estáticos de referencia (no pronostica clima ni precios). Apoya la decisión; no sustituye "
    "el criterio humano."
)


class ExportError(RuntimeError):
    """Excepción fail-fast si falta o falla cualquier salida obligatoria."""


def _plot_fitness_convergence(run: GARunResult, out_path: Path) -> None:
    gens = [s.generation for s in run.history]
    best = [s.best_fitness for s in run.history]
    mean = [s.mean_fitness for s in run.history]
    worst = [s.worst_fitness for s in run.history]

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    ax.plot(gens, best, label="Mejor Fitness", color="#1b7837", linewidth=2.4)
    ax.plot(gens, mean, label="Fitness Promedio", color="#2166ac", linewidth=1.8)
    ax.plot(gens, worst, label="Peor Fitness", color="#b2182b", linewidth=1.2, alpha=0.75)

    emp = run.baselines["baseline_empirical_rotation"].fitness
    mono = run.baselines["baseline_monoculture"].fitness
    ax.axhline(emp, color="#e08214", linestyle="--", linewidth=1.4, label=f"Línea Base Empírica ({emp:.4f})")
    ax.axhline(mono, color="#762a83", linestyle=":", linewidth=1.4, label=f"Línea Base Monocultivo ({mono:.4f})")

    ax.set_title(
        f"SAGE — Convergencia del Fitness ({run.run_id})\n"
        f"Escenario: {run.scenario_id} | seed={run.config.seed} | data_vintage={run.data_vintage}",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xlabel("Generación")
    ax.set_ylabel("Fitness Compuesto")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(loc="lower right", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def _plot_top3_nitrogen(run: GARunResult, scenario: ScenarioData, out_path: Path) -> None:
    cycles = list(range(scenario.env.total_cycles + 1))
    cycle_labels = ["C0"] + [f"C{i+1}\n{s}" for i, s in enumerate(scenario.env.cycle_seasons)]
    colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), dpi=150, sharey=True)
    for idx, (ax, ind) in enumerate(zip(axes, run.top_individuals), start=1):
        for p_idx, parcel in enumerate(scenario.parcels):
            ax.plot(
                cycles,
                ind.nitrogen_trajectory[p_idx],
                marker="o",
                markersize=3.5,
                linewidth=1.7,
                color=colors[p_idx % len(colors)],
                label=f"{parcel.parcel_id} ({parcel.area_ha:.1f} ha)",
            )
        ax.axhline(0.0, color="#b2182b", linestyle="--", linewidth=1.4, label="Umbral crítico N=0")
        ax.axhline(
            scenario.env.target_healthy_kg_ha,
            color="#2166ac",
            linestyle=":",
            linewidth=1.1,
            label=f"Meta saludable ({scenario.env.target_healthy_kg_ha:.0f})",
        )
        ax.set_title(
            f"Top-{idx} (Fitness={ind.fitness:.4f})\n"
            f"N final prom={ind.mean_final_nitrogen:.1f} | N mín={ind.min_nitrogen_any_cycle:.1f} kg/ha",
            fontsize=9.5,
            fontweight="bold",
        )
        ax.set_xticks(cycles)
        ax.set_xticklabels(cycle_labels, fontsize=7)
        ax.set_xlabel("Ciclo")
        ax.grid(True, linestyle="--", alpha=0.3)
        if idx == 1:
            ax.set_ylabel("Nitrógeno del Suelo (kg N/ha)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8, frameon=True)
    fig.suptitle(
        f"SAGE — Evolución de Nitrógeno del Suelo en Top-3 Individuos ({run.run_id} | seed={run.config.seed} | vintage={run.data_vintage})",
        fontsize=11,
        fontweight="bold",
    )
    fig.tight_layout(rect=[0, 0.11, 1, 0.94])
    fig.savefig(out_path)
    plt.close(fig)


def _plot_cost_vs_production(run: GARunResult, scenario: ScenarioData, out_path: Path) -> None:
    currency = scenario.env.currency
    entries: List[tuple[str, EvaluationResult]] = [
        ("LB Monocultivo", run.baselines["baseline_monoculture"]),
        ("LB Rot. Empírica", run.baselines["baseline_empirical_rotation"]),
        ("SAGE Top-1", run.top_individuals[0]),
        ("SAGE Top-2", run.top_individuals[1]),
        ("SAGE Top-3", run.top_individuals[2]),
    ]

    labels = [e[0] for e in entries]
    costs = [e[1].total_cost_mxn for e in entries]
    revs = [e[1].total_revenue_mxn for e in entries]
    profits = [e[1].net_profit_mxn for e in entries]

    x = np.arange(len(labels))
    width = 0.26

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=150)
    b1 = ax.bar(x - width, costs, width, label=f"Costo Operativo Total ({currency})", color="#d95f02")
    b2 = ax.bar(x, revs, width, label=f"Valor Bruto Producción ({currency})", color="#1b9e77")
    b3 = ax.bar(x + width, profits, width, label=f"Utilidad Neta ({currency})", color="#386cb0")

    for bars in (b1, b2, b3):
        for bar in bars:
            h = bar.get_height()
            offset_y = 3 if h >= 0 else -11
            ax.annotate(
                f"{h/1e6:.2f}M",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, offset_y),
                textcoords="offset points",
                ha="center",
                va="bottom" if h >= 0 else "top",
                fontsize=7.5,
            )

    ax.axhline(0.0, color="#333333", linewidth=0.9)
    ax.set_title(
        f"SAGE — Comparativa Costo vs. Producción y Utilidad Neta en {currency} (5 años / 10 ciclos)\n"
        f"{run.run_id} | Escenario: {run.scenario_id} | seed={run.config.seed} | vintage={run.data_vintage}",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(f"{currency} Acumulados (18.0 ha × 10 ciclos)")
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax.legend(loc="upper left", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def _plot_water_balance(run: GARunResult, scenario: ScenarioData, out_path: Path) -> None:
    cycles = np.arange(scenario.env.total_cycles)
    cycle_labels = [f"C{i+1}\n{s}" for i, s in enumerate(scenario.env.cycle_seasons)]
    width = 0.36

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), dpi=150, sharey=True)
    for idx, (ax, ind) in enumerate(zip(axes, run.top_individuals), start=1):
        ax.bar(
            cycles - width / 2,
            ind.water_required_by_cycle,
            width,
            label="Requerido (mm/ha)",
            color="#2b8cbe",
        )
        ax.bar(
            cycles + width / 2,
            ind.water_applied_by_cycle,
            width,
            label="Aplicado (mm/ha)",
            color="#a6bddb",
            edgecolor="#045a8d",
        )
        ax.set_title(
            f"Top-{idx} (Desvío prom={ind.mean_water_deviation_mm:.1f} mm)\n"
            f"Score hídrico={ind.score_water:.3f}",
            fontsize=9.5,
            fontweight="bold",
        )
        ax.set_xticks(cycles)
        ax.set_xticklabels(cycle_labels, fontsize=7.5)
        ax.set_xlabel("Ciclo")
        ax.grid(True, axis="y", linestyle="--", alpha=0.3)
        if idx == 1:
            ax.set_ylabel("Lámina Hídrica Ponderada (mm/ha)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, fontsize=9, frameon=True)
    fig.suptitle(
        f"SAGE — Balance Hídrico (Aplicado vs. Requerido) en Top-3 ({run.run_id} | seed={run.config.seed} | vintage={run.data_vintage})",
        fontsize=11,
        fontweight="bold",
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.94])
    fig.savefig(out_path)
    plt.close(fig)


def _build_summary_rows(run: GARunResult) -> List[Dict[str, object]]:
    ordered = [
        ("Baseline_Monocultivo", run.baselines["baseline_monoculture"]),
        ("Baseline_Rotacion_Empirica", run.baselines["baseline_empirical_rotation"]),
        ("SAGE_Top_1", run.top_individuals[0]),
        ("SAGE_Top_2", run.top_individuals[1]),
        ("SAGE_Top_3", run.top_individuals[2]),
    ]
    rows: List[Dict[str, object]] = []
    for name, ev in ordered:
        rows.append(
            {
                "plan_id": name,
                "run_id": run.run_id,
                "scenario_id": run.scenario_id,
                "seed": run.config.seed,
                "data_vintage": run.data_vintage,
                "fitness": round(ev.fitness, 6),
                "base_score": round(ev.base_score, 6),
                "penalty_total": round(ev.penalty_total, 6),
                "total_cost_mxn": round(ev.total_cost_mxn, 2),
                "total_revenue_mxn": round(ev.total_revenue_mxn, 2),
                "net_profit_mxn": round(ev.net_profit_mxn, 2),
                "total_production_ton": round(ev.total_production_ton, 2),
                "mean_final_nitrogen_kg_ha": round(ev.mean_final_nitrogen, 2),
                "min_nitrogen_any_cycle_kg_ha": round(ev.min_nitrogen_any_cycle, 2),
                "mean_water_deviation_mm": round(ev.mean_water_deviation_mm, 2),
                "nitrogen_violations": ev.nitrogen_violations,
                "season_violations": ev.season_violations,
                "monoculture_violations": ev.monoculture_violations,
                "feasible_nitrogen": ev.is_feasible_nitrogen,
            }
        )
    return rows


def _build_calendar_rows(run: GARunResult, scenario: ScenarioData) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for rank, ind in enumerate(run.top_individuals, start=1):
        for p_idx, parcel in enumerate(scenario.parcels):
            for t in range(scenario.env.total_cycles):
                cid = int(ind.chromosome[p_idx, t, 0])
                irr = int(ind.chromosome[p_idx, t, 1])
                crop = scenario.crops[cid]
                season = scenario.env.cycle_seasons[t]
                w_app = scenario.env.irrigation_levels_mm[irr]
                w_req = crop.water_req_mm[season]
                rows.append(
                    {
                        "individual": f"SAGE_Top_{rank}",
                        "parcel_id": parcel.parcel_id,
                        "area_ha": parcel.area_ha,
                        "cycle": t + 1,
                        "season": season,
                        "crop_id": cid,
                        "crop_name": crop.name,
                        "irrigation_level": irr,
                        "water_applied_mm": w_app,
                        "water_required_mm": w_req,
                        "water_deviation_mm": abs(w_app - w_req),
                        "nitrogen_post_kg_ha": round(float(ind.nitrogen_trajectory[p_idx, t + 1]), 2),
                    }
                )
    return rows


def _write_markdown_report(
    run: GARunResult,
    scenario: ScenarioData,
    summary_rows: List[Dict[str, object]],
    out_path: Path,
) -> None:
    d12 = hamming_distance(run.top_individuals[0].chromosome, run.top_individuals[1].chromosome)
    d13 = hamming_distance(run.top_individuals[0].chromosome, run.top_individuals[2].chromosome)
    d23 = hamming_distance(run.top_individuals[1].chromosome, run.top_individuals[2].chromosome)

    lines: List[str] = [
        f"# Reporte Operativo Top-3 (`DEC-01` / `DEC-02`) — {run.run_id}",
        "",
        f"- **Escenario:** `{run.scenario_id}` ({len(scenario.parcels)} parcelas × {scenario.env.total_cycles} ciclos `PV`/`OI`)",
        f"- **Semilla (`seed`):** `{run.config.seed}`",
        f"- **Frescura de datos (`data_vintage`):** `{run.data_vintage}`",
        f"- **Hiperparámetros:** población=`{run.config.population_size}`, generaciones=`{run.config.generations}`, cruce=`{run.config.crossover_rate}`, mutación=`{run.config.mutation_rate}`, torneo=`{run.config.tournament_size}`, elitismo=`{run.config.elitism_count}`",
        f"- **Diversidad estructural Top-3 (distancia de Hamming en 100 alelos):** `Top1-Top2={d12}`, `Top1-Top3={d13}`, `Top2-Top3={d23}`",
        "",
        f"> {PRESCRIPTIVE_NOTICE}",
        "",
        "## 1. Tabla Comparativa: Líneas Base vs. Top-3 de SAGE",
        "",
        "| Plan | Fitness | Costo Total (MXN) | Producción (ton) | Valor Bruto (MXN) | Utilidad Neta (MXN) | N Final Prom (kg/ha) | N Mín (kg/ha) | Desvío Hídrico Prom (mm) | Violaciones (N/Temp/Mono) |",
        "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |",
    ]

    for row in summary_rows:
        viol = f"{row['nitrogen_violations']}/{row['season_violations']}/{row['monoculture_violations']}"
        lines.append(
            f"| `{row['plan_id']}` | {row['fitness']:.4f} | {row['total_cost_mxn']:,.2f} | "
            f"{row['total_production_ton']:,.2f} | {row['total_revenue_mxn']:,.2f} | "
            f"{row['net_profit_mxn']:,.2f} | {row['mean_final_nitrogen_kg_ha']:.2f} | "
            f"{row['min_nitrogen_any_cycle_kg_ha']:.2f} | {row['mean_water_deviation_mm']:.2f} | {viol} |"
        )

    lines.extend(["", "## 2. Calendarios Parcela × Ciclo de los 3 Mejores Individuos (`DEC-02`)"])

    short_names = {0: "Barb", 1: "Maíz", 2: "Frij", 3: "Sorg", 4: "Av/Tr"}
    header_cols = " | ".join(
        [f"C{t+1} ({s})" for t, s in enumerate(scenario.env.cycle_seasons)]
    )
    sep_cols = " | ".join(["---"] * scenario.env.total_cycles)

    for rank, ind in enumerate(run.top_individuals, start=1):
        lines.extend(
            [
                "",
                f"### Individuo `SAGE_Top_{rank}` — Fitness `{ind.fitness:.4f}` | Utilidad Neta `{ind.net_profit_mxn:,.2f} MXN` | N Final Prom `{ind.mean_final_nitrogen:.2f} kg/ha` | Desvío Hídrico `{ind.mean_water_deviation_mm:.2f} mm`",
                "",
                f"| Parcela (Área / N0) | {header_cols} | N Final |",
                f"| :--- | {sep_cols} | ---: |",
            ]
        )
        for p_idx, parcel in enumerate(scenario.parcels):
            cells = []
            for t in range(scenario.env.total_cycles):
                cid = int(ind.chromosome[p_idx, t, 0])
                irr = int(ind.chromosome[p_idx, t, 1])
                mm = int(scenario.env.irrigation_levels_mm[irr])
                cells.append(f"{short_names[cid]} ({mm})")
            n_end = ind.final_nitrogen_by_parcel[p_idx]
            lines.append(
                f"| {parcel.parcel_id} ({parcel.area_ha:.1f}ha / {parcel.initial_nitrogen_kg_ha:.0f}) | "
                + " | ".join(cells)
                + f" | {n_end:.1f} |"
            )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_run_outputs(
    run: GARunResult,
    scenario: ScenarioData,
    output_dir: str | Path,
) -> Dict[str, Path]:
    """Exporta todas las salidas obligatorias y valida fail-fast su integridad."""
    if len(run.top_individuals) != 3:
        raise ExportError(f"Se requieren exactamente 3 individuos Top-K; recibidos {len(run.top_individuals)}.")

    out_root = Path(output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    paths: Dict[str, Path] = {
        "fitness_convergence_png": out_root / "fitness_convergence.png",
        "top3_nitrogen_png": out_root / "top3_nitrogen_evolution.png",
        "top3_cost_production_png": out_root / "top3_cost_vs_production.png",
        "top3_water_balance_png": out_root / "top3_water_balance.png",
        "top3_summary_csv": out_root / "top3_summary.csv",
        "top3_calendars_csv": out_root / "top3_calendars.csv",
        "top3_report_json": out_root / "top3_report.json",
        "top3_report_md": out_root / "top3_report.md",
    }

    _plot_fitness_convergence(run, paths["fitness_convergence_png"])
    _plot_top3_nitrogen(run, scenario, paths["top3_nitrogen_png"])
    _plot_cost_vs_production(run, scenario, paths["top3_cost_production_png"])
    _plot_water_balance(run, scenario, paths["top3_water_balance_png"])

    summary_rows = _build_summary_rows(run)
    calendar_rows = _build_calendar_rows(run, scenario)

    pd.DataFrame(summary_rows).to_csv(paths["top3_summary_csv"], index=False, encoding="utf-8")
    pd.DataFrame(calendar_rows).to_csv(paths["top3_calendars_csv"], index=False, encoding="utf-8")
    _write_markdown_report(run, scenario, summary_rows, paths["top3_report_md"])

    json_payload = {
        "run_id": run.run_id,
        "scenario_id": run.scenario_id,
        "data_vintage": run.data_vintage,
        "currency": scenario.env.currency,
        "seed": run.config.seed,
        "prescriptive_notice": PRESCRIPTIVE_NOTICE,
        "config": {
            "population_size": run.config.population_size,
            "generations": run.config.generations,
            "crossover_rate": run.config.crossover_rate,
            "mutation_rate": run.config.mutation_rate,
            "tournament_size": run.config.tournament_size,
            "elitism_count": run.config.elitism_count,
            "min_top3_hamming_distance": run.config.min_top3_hamming_distance,
            "penalty_overrides": run.config.penalty_overrides,
        },
        "convergence_history": [
            {
                "generation": s.generation,
                "best_fitness": round(s.best_fitness, 6),
                "mean_fitness": round(s.mean_fitness, 6),
                "worst_fitness": round(s.worst_fitness, 6),
                "feasible_ratio": round(s.feasible_ratio, 4),
            }
            for s in run.history
        ],
        "summary": summary_rows,
        "top3_calendars": calendar_rows,
    }
    paths["top3_report_json"].write_text(
        json.dumps(json_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Validación fail-fast de todas las salidas obligatorias
    for key, p in paths.items():
        if not p.exists() or p.stat().st_size == 0:
            raise ExportError(f"Fallo parcial de exportación: archivo '{key}' ausente o vacío en {p}.")

    return paths
