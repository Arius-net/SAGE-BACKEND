"""Cargador y validador fail-fast de la Base de Conocimiento de SAGE."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import numpy as np

from .models import Crop, EnvParams, Parcel, ScenarioData

REQUIRED_CROP_IDS = {0, 1, 2, 3, 4}
REQUIRED_IRRIGATION_LEVELS = {0, 1, 2, 3, 4}
VALID_SEASONS = {"PV", "OI"}
REQUIRED_WEIGHT_KEYS = {"w_production", "w_cost", "w_nitrogen", "w_water"}
REQUIRED_PENALTY_KEYS = {
    "nitrogen_depletion_per_violation",
    "out_of_season_per_violation",
    "consecutive_monoculture_per_violation",
}
REQUIRED_SCALE_KEYS = {
    "max_expected_revenue_per_ha_cycle",
    "max_expected_cost_per_ha_cycle",
    "max_expected_water_dev_mm_cycle",
}


class DataValidationError(ValueError):
    """Excepción fail-fast ante esquemas o valores inválidos."""


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise DataValidationError(f"Archivo obligatorio no encontrado: {path}")
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise DataValidationError(f"JSON inválido en {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise DataValidationError(f"La raíz de {path} debe ser un objeto JSON.")
    return data


def _require_non_empty_str(obj: Dict[str, Any], key: str, ctx: str) -> str:
    val = obj.get(key)
    if not isinstance(val, str) or not val.strip():
        raise DataValidationError(f"Campo '{key}' faltante o vacío en {ctx}.")
    return val.strip()


def _require_number(obj: Dict[str, Any], key: str, ctx: str, *, min_val: float | None = None, strict_min: bool = False) -> float:
    val = obj.get(key)
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise DataValidationError(f"Campo numérico '{key}' inválido en {ctx}: {val!r}")
    fval = float(val)
    if not np.isfinite(fval):
        raise DataValidationError(f"Campo '{key}' no finito en {ctx}.")
    if min_val is not None:
        if strict_min and fval <= min_val:
            raise DataValidationError(f"Campo '{key}' debe ser > {min_val} en {ctx} (recibido {fval}).")
        if not strict_min and fval < min_val:
            raise DataValidationError(f"Campo '{key}' debe ser >= {min_val} en {ctx} (recibido {fval}).")
    return fval


def load_crops_catalog(path: Path) -> tuple[Dict[int, Crop], str]:
    raw = _read_json(path)
    vintage = _require_non_empty_str(raw, "data_vintage", str(path))
    crops_list = raw.get("crops")
    if not isinstance(crops_list, list) or not crops_list:
        raise DataValidationError(f"'crops' debe ser una lista no vacía en {path}.")

    crops: Dict[int, Crop] = {}
    for idx, item in enumerate(crops_list):
        ctx = f"{path}:crops[{idx}]"
        if not isinstance(item, dict):
            raise DataValidationError(f"Entrada inválida en {ctx}.")
        cid = item.get("crop_id")
        if isinstance(cid, bool) or not isinstance(cid, int):
            raise DataValidationError(f"'crop_id' debe ser entero en {ctx}.")
        if cid in crops:
            raise DataValidationError(f"'crop_id' duplicado ({cid}) en {path}.")

        name = _require_non_empty_str(item, "name", ctx)
        category = _require_non_empty_str(item, "category", ctx)
        seasons = item.get("compatible_seasons")
        if not isinstance(seasons, list) or not seasons or not set(seasons).issubset(VALID_SEASONS):
            raise DataValidationError(f"'compatible_seasons' inválido en {ctx}: {seasons!r}")

        water_req = item.get("water_req_mm")
        if not isinstance(water_req, dict) or set(water_req.keys()) != VALID_SEASONS:
            raise DataValidationError(f"'water_req_mm' debe definir exactamente PV y OI en {ctx}.")
        water_req_clean = {
            "PV": _require_number(water_req, "PV", f"{ctx}.water_req_mm", min_val=0.0),
            "OI": _require_number(water_req, "OI", f"{ctx}.water_req_mm", min_val=0.0),
        }

        crops[cid] = Crop(
            crop_id=cid,
            name=name,
            category=category,
            compatible_seasons=tuple(seasons),
            base_cost_mxn_ha=_require_number(item, "base_cost_mxn_ha", ctx, min_val=0.0),
            nominal_yield_ton_ha=_require_number(item, "nominal_yield_ton_ha", ctx, min_val=0.0),
            reference_price_mxn_ton=_require_number(item, "reference_price_mxn_ton", ctx, min_val=0.0),
            nitrogen_delta_kg_ha=_require_number(item, "nitrogen_delta_kg_ha", ctx),
            water_req_mm=water_req_clean,
        )

    if set(crops.keys()) != REQUIRED_CROP_IDS:
        raise DataValidationError(
            f"El catálogo de cultivos debe contener exactamente los IDs {sorted(REQUIRED_CROP_IDS)}; "
            f"recibidos {sorted(crops.keys())}."
        )
    return crops, vintage


def load_env_params(path: Path) -> EnvParams:
    raw = _read_json(path)
    schema_version = _require_non_empty_str(raw, "schema_version", str(path))
    vintage = _require_non_empty_str(raw, "data_vintage", str(path))

    horizon = raw.get("horizon")
    if not isinstance(horizon, dict):
        raise DataValidationError(f"Sección 'horizon' faltante en {path}.")
    years = horizon.get("years")
    cpy = horizon.get("cycles_per_year")
    total_cycles = horizon.get("total_cycles")
    seasons = horizon.get("cycle_seasons")
    if years != 5 or cpy != 2 or total_cycles != 10:
        raise DataValidationError(f"El horizonte debe ser 5 años / 2 ciclos por año / 10 ciclos totales en {path}.")
    if not isinstance(seasons, list) or len(seasons) != 10:
        raise DataValidationError(f"'cycle_seasons' debe contener exactamente 10 ciclos en {path}.")
    expected_seasons = ["PV" if i % 2 == 0 else "OI" for i in range(10)]
    if seasons != expected_seasons:
        raise DataValidationError(f"'cycle_seasons' debe alternar PV/OI empezando en PV en {path}.")

    irr_raw = raw.get("irrigation_levels_mm")
    if not isinstance(irr_raw, dict):
        raise DataValidationError(f"Sección 'irrigation_levels_mm' faltante en {path}.")
    irr_levels: Dict[int, float] = {}
    for k, v in irr_raw.items():
        try:
            ik = int(k)
        except (TypeError, ValueError) as exc:
            raise DataValidationError(f"Clave de riego no entera '{k}' en {path}.") from exc
        if isinstance(v, bool) or not isinstance(v, (int, float)) or float(v) < 0.0:
            raise DataValidationError(f"Valor de riego inválido para nivel {k} en {path}.")
        irr_levels[ik] = float(v)
    if set(irr_levels.keys()) != REQUIRED_IRRIGATION_LEVELS:
        raise DataValidationError(
            f"'irrigation_levels_mm' debe definir exactamente niveles {sorted(REQUIRED_IRRIGATION_LEVELS)}."
        )

    econ = raw.get("economics", {})
    soil = raw.get("soil_nitrogen", {})
    agro = raw.get("agronomic_factors", {})
    weights_raw = raw.get("fitness_weights", {})
    penalties_raw = raw.get("penalties", {})
    scales_raw = raw.get("normalization_scales", {})

    if not isinstance(weights_raw, dict) or set(weights_raw.keys()) != REQUIRED_WEIGHT_KEYS:
        raise DataValidationError(f"'fitness_weights' debe contener exactamente {sorted(REQUIRED_WEIGHT_KEYS)}.")
    weights = {k: _require_number(weights_raw, k, f"{path}.fitness_weights", min_val=0.0) for k in REQUIRED_WEIGHT_KEYS}
    if abs(sum(weights.values()) - 1.0) > 1e-6:
        raise DataValidationError(f"Los pesos en 'fitness_weights' deben sumar 1.0 (suma={sum(weights.values())}).")

    if not isinstance(penalties_raw, dict) or set(penalties_raw.keys()) != REQUIRED_PENALTY_KEYS:
        raise DataValidationError(f"'penalties' debe contener exactamente {sorted(REQUIRED_PENALTY_KEYS)}.")
    penalties = {k: _require_number(penalties_raw, k, f"{path}.penalties", min_val=0.0) for k in REQUIRED_PENALTY_KEYS}

    if not isinstance(scales_raw, dict) or set(scales_raw.keys()) != REQUIRED_SCALE_KEYS:
        raise DataValidationError(f"'normalization_scales' debe contener exactamente {sorted(REQUIRED_SCALE_KEYS)}.")
    scales = {k: _require_number(scales_raw, k, f"{path}.normalization_scales", min_val=0.0, strict_min=True) for k in REQUIRED_SCALE_KEYS}

    return EnvParams(
        schema_version=schema_version,
        data_vintage=vintage,
        years=years,
        cycles_per_year=cpy,
        total_cycles=total_cycles,
        cycle_seasons=tuple(seasons),
        irrigation_levels_mm=irr_levels,
        water_cost_mxn_per_mm_ha=_require_number(econ, "water_cost_mxn_per_mm_ha", f"{path}.economics", min_val=0.0),
        currency=_require_non_empty_str(econ, "currency", f"{path}.economics"),
        critical_min_kg_ha=_require_number(soil, "critical_min_kg_ha", f"{path}.soil_nitrogen", min_val=0.0),
        target_healthy_kg_ha=_require_number(soil, "target_healthy_kg_ha", f"{path}.soil_nitrogen", min_val=0.0, strict_min=True),
        max_capacity_kg_ha=_require_number(soil, "max_capacity_kg_ha", f"{path}.soil_nitrogen", min_val=0.0, strict_min=True),
        depleted_yield_factor=_require_number(agro if "depleted_yield_factor" in agro else soil, "depleted_yield_factor", f"{path}.soil_nitrogen", min_val=0.0),
        out_of_season_yield_factor=_require_number(agro, "out_of_season_yield_factor", f"{path}.agronomic_factors", min_val=0.0),
        monoculture_yield_factor=_require_number(agro, "monoculture_yield_factor", f"{path}.agronomic_factors", min_val=0.0),
        min_water_stress_yield_factor=_require_number(agro, "min_water_stress_yield_factor", f"{path}.agronomic_factors", min_val=0.0),
        fitness_weights=weights,
        penalties=penalties,
        normalization_scales=scales,
    )


def load_parcels_input(path: Path, critical_min_n: float = 0.0) -> tuple[tuple[Parcel, ...], str, str]:
    raw = _read_json(path)
    vintage = _require_non_empty_str(raw, "data_vintage", str(path))
    scenario_id = _require_non_empty_str(raw, "scenario_id", str(path))
    plist = raw.get("parcels")
    if not isinstance(plist, list) or not (3 <= len(plist) <= 10):
        raise DataValidationError(f"'parcels' debe tener entre 3 y 10 parcelas en {path}.")

    seen_ids: set[str] = set()
    parcels: list[Parcel] = []
    for idx, item in enumerate(plist):
        ctx = f"{path}:parcels[{idx}]"
        if not isinstance(item, dict):
            raise DataValidationError(f"Entrada inválida en {ctx}.")
        pid = _require_non_empty_str(item, "parcel_id", ctx)
        if pid in seen_ids:
            raise DataValidationError(f"'parcel_id' duplicado '{pid}' en {path}.")
        seen_ids.add(pid)
        parcels.append(
            Parcel(
                parcel_id=pid,
                name=_require_non_empty_str(item, "name", ctx),
                area_ha=_require_number(item, "area_ha", ctx, min_val=0.0, strict_min=True),
                initial_nitrogen_kg_ha=_require_number(
                    item, "initial_nitrogen_kg_ha", ctx, min_val=critical_min_n, strict_min=True
                ),
                soil_profile=_require_non_empty_str(item, "soil_profile", ctx),
            )
        )
    return tuple(parcels), scenario_id, vintage


def load_scenario(data_dir: str | Path) -> ScenarioData:
    """Carga y valida en modo fail-fast los tres archivos de la Base de Conocimiento."""
    base = Path(data_dir)
    crops, crops_vintage = load_crops_catalog(base / "crops_catalog.json")
    env = load_env_params(base / "env_params.json")
    parcels, scenario_id, parcels_vintage = load_parcels_input(
        base / "parcels_input.json", critical_min_n=env.critical_min_kg_ha
    )
    if len({crops_vintage, env.data_vintage, parcels_vintage}) != 1:
        raise DataValidationError(
            f"Inconsistencia de data_vintage entre archivos: "
            f"crops={crops_vintage}, env={env.data_vintage}, parcels={parcels_vintage}"
        )
    return ScenarioData(
        scenario_id=scenario_id,
        data_vintage=env.data_vintage,
        crops=crops,
        env=env,
        parcels=parcels,
    )


def validate_chromosome(chromosome: np.ndarray, scenario: ScenarioData) -> None:
    """Valida fail-fast forma, tipo entero y dominio cerrado {0..4} del cromosoma."""
    expected_shape = (len(scenario.parcels), scenario.env.total_cycles, 2)
    if not isinstance(chromosome, np.ndarray) or chromosome.shape != expected_shape:
        raise DataValidationError(
            f"Cromosoma con forma inválida: esperado {expected_shape}, recibido {getattr(chromosome, 'shape', None)}."
        )
    if not np.issubdtype(chromosome.dtype, np.integer):
        raise DataValidationError(f"El cromosoma debe tener tipo entero; recibido {chromosome.dtype}.")
    crops_vals = chromosome[:, :, 0]
    irr_vals = chromosome[:, :, 1]
    if np.any((crops_vals < 0) | (crops_vals > 4)):
        raise DataValidationError("Cromosoma contiene crop_id fuera de dominio {0..4}.")
    if np.any((irr_vals < 0) | (irr_vals > 4)):
        raise DataValidationError("Cromosoma contiene irrigation_level fuera de dominio {0..4}.")
