"""
pytest data/app_data/10-rl-alignment/03-fine-tuning/02-full-finetune-vs-lora-comparison/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/03-fine-tuning/{Path(__file__).resolve().parent.name}")
full_finetune_parameter_count = _module.full_finetune_parameter_count
lora_parameter_count = _module.lora_parameter_count
optimizer_state_bytes = _module.optimizer_state_bytes
compare_full_finetune_vs_lora = _module.compare_full_finetune_vs_lora


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_full_finetune_count_matches_hand_computation():
    assert full_finetune_parameter_count(in_features=10, out_features=20) == 220


def test_02_lora_uses_far_fewer_parameters_for_realistic_dimensions():
    comparison = compare_full_finetune_vs_lora(in_features=4096, out_features=4096, rank=16)
    assert comparison["lora_params"] < comparison["full_finetune_params"] / 100


# --- General-case coverage --------------------------------------------


def test_03_lora_parameter_count_matches_hand_computation():
    assert lora_parameter_count(in_features=10, out_features=20, rank=4) == 4 * 10 + 20 * 4


def test_04_optimizer_state_bytes_scales_linearly():
    assert optimizer_state_bytes(1000) == 8000
    assert optimizer_state_bytes(0) == 0


def test_05_parameter_reduction_factor_matches_ratio():
    comparison = compare_full_finetune_vs_lora(in_features=100, out_features=100, rank=4)
    assert math.isclose(
        comparison["parameter_reduction_factor"], comparison["full_finetune_params"] / comparison["lora_params"]
    )


# --- Parameter handling -------------------------------------------------


def test_06_frozen_base_parameters_need_no_optimizer_state():
    # A full fine-tune's optimizer memory must be strictly LARGER than
    # LoRA's for the same layer, since LoRA's frozen base weight
    # contributes zero optimizer bytes.
    comparison = compare_full_finetune_vs_lora(in_features=512, out_features=512, rank=8)
    assert comparison["lora_optimizer_bytes"] < comparison["full_finetune_optimizer_bytes"]


def test_07_optimizer_bytes_derived_from_the_matching_parameter_counts():
    comparison = compare_full_finetune_vs_lora(in_features=64, out_features=32, rank=2)
    assert comparison["full_finetune_optimizer_bytes"] == optimizer_state_bytes(comparison["full_finetune_params"])
    assert comparison["lora_optimizer_bytes"] == optimizer_state_bytes(comparison["lora_params"])


# --- Edge cases ---------------------------------------------------------


def test_08_rank_one_is_the_most_extreme_reduction():
    comparison = compare_full_finetune_vs_lora(in_features=1000, out_features=1000, rank=1)
    assert comparison["parameter_reduction_factor"] > 400


def test_09_square_layer_shape():
    assert full_finetune_parameter_count(50, 50) == 50 * 50 + 50


# --- Independent correctness oracle -----------------------------------


def test_10_full_finetune_count_includes_the_bias_term():
    # Directly targets a mutant that forgets the "+ out_features" bias
    # term, which would understate a full fine-tune's true parameter
    # count (a real, if small, difference that compounds across many
    # layers in a real transformer).
    without_bias = 10 * 20
    with_bias = full_finetune_parameter_count(10, 20)
    assert with_bias == without_bias + 20
    assert with_bias != without_bias
