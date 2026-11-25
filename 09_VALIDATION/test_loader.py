"""Pruebas fail-fast del cargador y validador de esquemas de SAGE."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
import pytest

from sage.loader import DataValidationError, load_scenario, validate_chromosome

DATA_REF = Path(__file__).resolve().parents[1] / "05_DATA" / "reference"


def test_load_reference_scenario_success() -> None:
    scenario = load_scenario(DATA_REF)
    assert scenario.scenario_id == "PILOT_5P_10C"
    assert scenario.data_vintage == "2026-11-23"
    assert len(scenario.parcels) == 5
    assert set(scenario.crops.keys()) == {0, 1, 2, 3, 4}
    assert scenario.env.total_cycles == 10


def test_fail_fast_missing_crop_id(tmp_path: Path) -> None:
    shutil.copytree(DATA_REF, tmp_path / "ref")
    crops_path = tmp_path / "ref" / "crops_catalog.json"
    data = json.loads(crops_path.read_text(encoding="utf-8"))
    data["crops"] = [c for c in data["crops"] if c["crop_id"] != 4]
    crops_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(DataValidationError, match="IDs"):
        load_scenario(tmp_path / "ref")


def test_fail_fast_invalid_parcel_nitrogen(tmp_path: Path) -> None:
    shutil.copytree(DATA_REF, tmp_path / "ref")
    parcels_path = tmp_path / "ref" / "parcels_input.json"
    data = json.loads(parcels_path.read_text(encoding="utf-8"))
    data["parcels"][0]["initial_nitrogen_kg_ha"] = 0.0
    parcels_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(DataValidationError, match="initial_nitrogen_kg_ha"):
        load_scenario(tmp_path / "ref")


def test_fail_fast_invalid_weights_sum(tmp_path: Path) -> None:
    shutil.copytree(DATA_REF, tmp_path / "ref")
    env_path = tmp_path / "ref" / "env_params.json"
    data = json.loads(env_path.read_text(encoding="utf-8"))
    data["fitness_weights"]["w_production"] = 0.90
    env_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(DataValidationError, match="sumar 1.0"):
        load_scenario(tmp_path / "ref")


def test_fail_fast_mismatched_data_vintage(tmp_path: Path) -> None:
    shutil.copytree(DATA_REF, tmp_path / "ref")
    env_path = tmp_path / "ref" / "env_params.json"
    data = json.loads(env_path.read_text(encoding="utf-8"))
    data["data_vintage"] = "2026-12-01"
    env_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(DataValidationError, match="data_vintage"):
        load_scenario(tmp_path / "ref")


def test_validate_chromosome_rejects_out_of_domain() -> None:
    scenario = load_scenario(DATA_REF)
    bad = np.zeros((5, 10, 2), dtype=np.int32)
    bad[0, 0, 0] = 5  # Fuera de {0..4}
    with pytest.raises(DataValidationError, match="crop_id"):
        validate_chromosome(bad, scenario)

    bad2 = np.zeros((5, 10, 2), dtype=np.int32)
    bad2[2, 4, 1] = -1  # Fuera de {0..4}
    with pytest.raises(DataValidationError, match="irrigation_level"):
        validate_chromosome(bad2, scenario)
