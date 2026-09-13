"""
pytest data/app_data/08-systems-performance/01-profiling/03-memory-footprint-estimation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/01-profiling/{Path(__file__).resolve().parent.name}")
estimate_memory_bytes = _module.estimate_memory_bytes
estimate_optimizer_memory_bytes = _module.estimate_optimizer_memory_bytes


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_float32_uses_4_bytes_per_element():
    params = [np.zeros((10,))]
    assert estimate_memory_bytes(params, "float32") == 40


def test_02_int8_uses_1_byte_per_element():
    params = [np.zeros((10,))]
    assert estimate_memory_bytes(params, "int8") == 10


# --- Shape / general-case coverage -----------------------------------


def test_03_float16_and_bfloat16_both_use_2_bytes_per_element():
    params = [np.zeros((100,))]
    assert estimate_memory_bytes(params, "float16") == 200
    assert estimate_memory_bytes(params, "bfloat16") == 200


def test_04_multiple_arrays_sum_before_scaling_by_dtype():
    params = [np.zeros((4, 10)), np.zeros(4)]  # 44 elements total
    assert estimate_memory_bytes(params, "float32") == 44 * 4


# --- Parameter handling -------------------------------------------------


def test_05_lower_precision_gives_proportionally_smaller_footprint():
    params = [np.zeros((1000,))]
    fp32_bytes = estimate_memory_bytes(params, "float32")
    int8_bytes = estimate_memory_bytes(params, "int8")
    assert fp32_bytes == 4 * int8_bytes  # int8 uses 1/4 the memory of float32


def test_06_optimizer_memory_defaults_to_params_plus_gradients_for_sgd():
    params = [np.zeros((100,))]
    param_bytes = estimate_memory_bytes(params, "float32")
    total = estimate_optimizer_memory_bytes(params, "float32", optimizer="sgd")
    assert total == param_bytes * 2  # params + gradients, no optimizer state


def test_07_adam_needs_four_times_the_raw_parameter_memory():
    # params + gradients + 2 moment estimates = 4x param_bytes
    params = [np.zeros((100,))]
    param_bytes = estimate_memory_bytes(params, "float32")
    total = estimate_optimizer_memory_bytes(params, "float32", optimizer="adam")
    assert total == param_bytes * 4


def test_08_momentum_needs_three_times_the_raw_parameter_memory():
    params = [np.zeros((100,))]
    param_bytes = estimate_memory_bytes(params, "float32")
    total = estimate_optimizer_memory_bytes(params, "float32", optimizer="momentum")
    assert total == param_bytes * 3


# --- Edge cases ---------------------------------------------------------


def test_09_empty_parameter_list_gives_zero_bytes():
    assert estimate_memory_bytes([], "float32") == 0
    assert estimate_optimizer_memory_bytes([], "float32", "adam") == 0


# --- Array hygiene ------------------------------------------------------


def test_10_does_not_mutate_the_input_arrays():
    weight = np.zeros((3, 4))
    weight_copy = weight.copy()
    estimate_memory_bytes([weight], "float32")
    assert np.array_equal(weight, weight_copy)


# --- Independent correctness oracle -----------------------------------


def test_11_matches_real_pytorch_element_sizes_for_every_supported_dtype():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   for dt in [torch.float32, torch.float16, torch.bfloat16, torch.int8]:
    #       torch.zeros(1, dtype=dt).element_size()
    #   # 4, 2, 2, 1 respectively
    #
    # This test needs no torch installed to run.
    params = [np.zeros((1,))]
    expected_bytes_per_element = {"float32": 4, "float16": 2, "bfloat16": 2, "int8": 1}
    for dtype, expected in expected_bytes_per_element.items():
        assert estimate_memory_bytes(params, dtype) == expected
