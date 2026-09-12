"""
pytest data/app_data/06-inference/03-quantization-and-numerical-efficiency/03-groupwise-int4-quantization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize_int4_groupwise = load_solution(
    f"06-inference/03-quantization-and-numerical-efficiency/{Path(__file__).resolve().parent.name}"
).quantize_int4_groupwise


def test_one_row_two_groups():
    result = quantize_int4_groupwise(np.array([[1.0, 2.0, -10.0, -20.0]]), group_size=2)
    assert result["scale"].shape == (1, 2)
    # Group 0 ([1,2]) and group 1 ([-10,-20]) must get different scales.
    assert not np.isclose(result["scale"][0, 0], result["scale"][0, 1])


def test_quantized_values_within_int4_range():
    rng = np.random.default_rng(0)
    W = rng.normal(size=(2, 4)) * np.array([[1], [50]])
    result = quantize_int4_groupwise(W, group_size=2)
    assert np.all(result["quantized"] >= -7)
    assert np.all(result["quantized"] <= 7)


def test_two_rows_two_groups_each():
    result = quantize_int4_groupwise(np.array([[1, 1, 1, 1], [0.1, -0.1, 5, -5]]), group_size=2)
    assert result["quantized"].shape == (2, 4)
    assert result["scale"].shape == (2, 2)
    # Row 1's second group (magnitude 5) must reach the INT4 edge (7).
    assert 7 in np.abs(result["quantized"][1, 2:4])


def test_group_size_equals_in_features_falls_back_to_per_row():
    result = quantize_int4_groupwise(np.array([[1.0, 2.0, 3.0, 4.0]]), group_size=4)
    assert result["scale"].shape == (1, 1)
    assert np.isclose(result["scale"][0, 0], 4.0 / 7)


def test_reconstruction_error_bounded_per_group():
    rng = np.random.default_rng(1)
    W = rng.normal(size=(3, 8))
    group_size = 4
    result = quantize_int4_groupwise(W, group_size)
    n_groups = 8 // group_size
    for row in range(3):
        for g in range(n_groups):
            sl = slice(g * group_size, (g + 1) * group_size)
            error = np.abs(W[row, sl] - result["dequantized"][row, sl])
            assert np.all(error <= result["scale"][row, g] / 2 + 1e-9)
