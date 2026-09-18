"""
pytest data/app_data/11-production-ml/01-experiment-tracking-and-versioning/03-model-registry-versioning/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/01-experiment-tracking-and-versioning/{Path(__file__).resolve().parent.name}")
create_registry = _module.create_registry
register_model_version = _module.register_model_version
promote_to_stage = _module.promote_to_stage
get_version_at_stage = _module.get_version_at_stage


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_register_assigns_sequential_version_numbers():
    registry = create_registry()
    register_model_version(registry, "spam-classifier", "run-a", {"f1": 0.8})
    register_model_version(registry, "spam-classifier", "run-b", {"f1": 0.85})
    versions = [v["version"] for v in registry["spam-classifier"]]
    assert versions == [1, 2]


def test_02_promote_to_production_makes_it_retrievable():
    registry = create_registry()
    register_model_version(registry, "m", "run-a", {})
    promote_to_stage(registry, "m", version=1, stage="production")
    prod = get_version_at_stage(registry, "m", "production")
    assert prod["version"] == 1


# --- General-case coverage --------------------------------------------


def test_03_new_production_version_archives_the_old_one():
    registry = create_registry()
    register_model_version(registry, "m", "run-a", {})
    register_model_version(registry, "m", "run-b", {})
    promote_to_stage(registry, "m", version=1, stage="production")
    promote_to_stage(registry, "m", version=2, stage="production")
    v1 = next(v for v in registry["m"] if v["version"] == 1)
    v2 = next(v for v in registry["m"] if v["version"] == 2)
    assert v1["stage"] == "archived"
    assert v2["stage"] == "production"


def test_04_new_versions_start_at_stage_none():
    registry = create_registry()
    register_model_version(registry, "m", "run-a", {})
    assert registry["m"][0]["stage"] == "none"


def test_05_metrics_are_preserved_per_version():
    registry = create_registry()
    register_model_version(registry, "m", "run-a", {"accuracy": 0.9})
    assert registry["m"][0]["metrics"] == {"accuracy": 0.9}


# --- Parameter handling -------------------------------------------------


def test_06_promoting_to_staging_does_not_touch_production():
    registry = create_registry()
    register_model_version(registry, "m", "run-a", {})
    register_model_version(registry, "m", "run-b", {})
    promote_to_stage(registry, "m", version=1, stage="production")
    promote_to_stage(registry, "m", version=2, stage="staging")
    v1 = next(v for v in registry["m"] if v["version"] == 1)
    assert v1["stage"] == "production"


def test_07_invalid_stage_raises():
    registry = create_registry()
    register_model_version(registry, "m", "run-a", {})
    with pytest.raises(ValueError):
        promote_to_stage(registry, "m", version=1, stage="not-a-real-stage")


# --- Edge cases ---------------------------------------------------------


def test_08_get_version_at_stage_returns_none_when_nothing_matches():
    registry = create_registry()
    register_model_version(registry, "m", "run-a", {})
    assert get_version_at_stage(registry, "m", "production") is None


def test_09_two_different_models_have_independent_version_numbering():
    registry = create_registry()
    register_model_version(registry, "model-a", "run-1", {})
    register_model_version(registry, "model-b", "run-2", {})
    assert registry["model-a"][0]["version"] == 1
    assert registry["model-b"][0]["version"] == 1


# --- Independent correctness oracle -----------------------------------


def test_10_only_one_production_version_can_ever_exist_at_once():
    # Directly targets a mutant that forgets to demote the previous
    # production version (letting two versions both claim
    # "production" simultaneously) -- across many successive
    # promotions, there must never be more than one production entry.
    registry = create_registry()
    for i in range(5):
        register_model_version(registry, "m", f"run-{i}", {})
    for version in range(1, 6):
        promote_to_stage(registry, "m", version=version, stage="production")
        production_versions = [v for v in registry["m"] if v["stage"] == "production"]
        assert len(production_versions) == 1
        assert production_versions[0]["version"] == version
