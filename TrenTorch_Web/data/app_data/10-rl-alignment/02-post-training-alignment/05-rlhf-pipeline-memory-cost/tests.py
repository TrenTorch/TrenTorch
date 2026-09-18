"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/05-rlhf-pipeline-memory-cost/tests.py
"""

import sys
from pathlib import Path

import math

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
models_required_for_stage = _module.models_required_for_stage
stage_memory_bytes = _module.stage_memory_bytes
ppo_memory_multiplier_over_sft = _module.ppo_memory_multiplier_over_sft
dpo_memory_multiplier_over_ppo = _module.dpo_memory_multiplier_over_ppo


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_ppo_needs_four_models_sft_needs_one():
    assert models_required_for_stage("ppo") == 4
    assert models_required_for_stage("sft") == 1


def test_02_ppo_memory_multiplier_over_sft_is_four():
    assert math.isclose(ppo_memory_multiplier_over_sft(), 4.0)


# --- General-case coverage --------------------------------------------


def test_03_dpo_needs_two_models():
    assert models_required_for_stage("dpo") == 2


def test_04_stage_memory_scales_by_model_count():
    assert math.isclose(stage_memory_bytes("ppo", 1000.0), 4000.0)
    assert math.isclose(stage_memory_bytes("sft", 1000.0), 1000.0)


def test_05_dpo_memory_multiplier_over_ppo_is_half():
    assert math.isclose(dpo_memory_multiplier_over_ppo(), 0.5)


# --- Parameter handling -------------------------------------------------


def test_06_reward_modeling_and_pretraining_need_one_model_each():
    assert models_required_for_stage("reward_modeling") == 1
    assert models_required_for_stage("pretraining") == 1


def test_07_unknown_stage_raises():
    with pytest.raises(ValueError):
        models_required_for_stage("not_a_real_stage")


# --- Edge cases ---------------------------------------------------------


def test_08_stage_memory_zero_model_size():
    assert stage_memory_bytes("ppo", 0.0) == 0.0


def test_09_dpo_uses_strictly_less_memory_than_ppo():
    assert models_required_for_stage("dpo") < models_required_for_stage("ppo")


# --- Independent correctness oracle -----------------------------------


def test_10_memory_ordering_matches_real_rlhf_pipeline_complexity():
    # Directly targets a mutant that mixes up which stage needs more
    # models (e.g. swapping dpo and ppo's counts): the real ordering
    # must be pretraining == sft == reward_modeling < dpo < ppo.
    counts = {stage: models_required_for_stage(stage) for stage in ("pretraining", "sft", "reward_modeling", "dpo", "ppo")}
    assert counts["pretraining"] == counts["sft"] == counts["reward_modeling"] == 1
    assert counts["dpo"] > counts["sft"]
    assert counts["ppo"] > counts["dpo"]
