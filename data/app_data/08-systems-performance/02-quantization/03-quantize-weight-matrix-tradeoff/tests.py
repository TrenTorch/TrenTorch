"""
pytest data/app_data/08-systems-performance/02-quantization/03-quantize-weight-matrix-tradeoff/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize_weight_matrix = load_solution(
    f"08-systems-performance/02-quantization/{Path(__file__).resolve().parent.name}"
).quantize_weight_matrix


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_compression_ratio_is_exactly_4x_for_float32_to_int8():
    weight = np.random.default_rng(0).normal(size=(10, 10)).astype(np.float32)
    result = quantize_weight_matrix(weight)
    assert np.isclose(result["compression_ratio"], 4.0)


def test_02_quantized_array_has_the_same_shape_as_the_input():
    weight = np.random.default_rng(1).normal(size=(4, 8)).astype(np.float32)
    result = quantize_weight_matrix(weight)
    assert result["quantized"].shape == weight.shape
    assert result["quantized"].dtype == np.int8


# --- Shape / general-case coverage -----------------------------------


def test_03_larger_matrix_still_gives_the_same_4x_compression_ratio():
    weight = np.random.default_rng(2).normal(size=(100, 200)).astype(np.float32)
    result = quantize_weight_matrix(weight)
    assert np.isclose(result["compression_ratio"], 4.0)


def test_04_errors_are_returned_as_plain_floats():
    weight = np.random.default_rng(3).normal(size=(5, 5)).astype(np.float32)
    result = quantize_weight_matrix(weight)
    assert isinstance(result["max_abs_error"], float)
    assert isinstance(result["mean_abs_error"], float)


# --- Parameter handling -------------------------------------------------


def test_05_max_error_is_never_smaller_than_mean_error():
    weight = np.random.default_rng(4).normal(size=(20, 20)).astype(np.float32)
    result = quantize_weight_matrix(weight)
    assert result["max_abs_error"] >= result["mean_abs_error"]


def test_06_a_wider_valued_matrix_has_a_larger_max_error():
    # A wider spread of values needs a coarser scale (to cover the same
    # int8 range), which means a larger worst-case rounding error.
    narrow = np.random.default_rng(5).normal(scale=0.1, size=(50, 50)).astype(np.float32)
    wide = np.random.default_rng(5).normal(scale=100.0, size=(50, 50)).astype(np.float32)
    narrow_result = quantize_weight_matrix(narrow)
    wide_result = quantize_weight_matrix(wide)
    assert wide_result["max_abs_error"] > narrow_result["max_abs_error"]


# --- Edge cases ---------------------------------------------------------


def test_07_constant_weight_matrix_has_zero_reconstruction_error():
    weight = np.full((5, 5), 3.0, dtype=np.float32)
    result = quantize_weight_matrix(weight)
    assert np.isclose(result["max_abs_error"], 0.0)


def test_08_single_element_matrix_works():
    weight = np.array([[7.0]], dtype=np.float32)
    result = quantize_weight_matrix(weight)
    assert result["quantized"].shape == (1, 1)


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_input():
    weight = np.random.default_rng(6).normal(size=(5, 5)).astype(np.float32)
    weight_copy = weight.copy()
    quantize_weight_matrix(weight)
    assert np.array_equal(weight, weight_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_reconstruction_error_stays_small_relative_to_a_real_linear_layers_weight_scale():
    # torch.nn.Linear's default (Kaiming uniform) init draws weights
    # from roughly [-1/sqrt(fan_in), 1/sqrt(fan_in)] -- for fan_in=256
    # that's about [-0.0625, 0.0625], a real, documented PyTorch default,
    # not a fabricated range. Quantizing a matrix in that realistic
    # range to int8 (256 total steps across the full observed range)
    # should keep the worst-case error to a small fraction of the
    # weights' own scale -- the actual practical basis for "int8
    # quantization barely hurts accuracy."
    rng = np.random.default_rng(7)
    weight = rng.uniform(-0.0625, 0.0625, size=(256, 256)).astype(np.float32)
    result = quantize_weight_matrix(weight)
    weight_range = weight.max() - weight.min()
    assert result["max_abs_error"] < weight_range * 0.01
