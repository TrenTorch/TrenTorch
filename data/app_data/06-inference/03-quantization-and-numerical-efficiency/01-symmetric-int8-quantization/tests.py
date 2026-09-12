"""
pytest data/app_data/06-inference/03-quantization-and-numerical-efficiency/01-symmetric-int8-quantization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize_int8_symmetric = load_solution(
    f"06-inference/03-quantization-and-numerical-efficiency/{Path(__file__).resolve().parent.name}"
).quantize_int8_symmetric


def test_basic_mixed_sign_tensor():
    result = quantize_int8_symmetric(np.array([1.0, -2.0, 0.5]))
    assert np.isclose(result["scale"], 2.0 / 127, atol=1e-6)
    assert result["quantized"][1] == -127  # the max-magnitude value hits the edge exactly
    assert np.allclose(result["dequantized"], [1.0, -2.0, 0.5], atol=0.02)


def test_all_zeros():
    result = quantize_int8_symmetric(np.array([0.0, 0.0, 0.0]))
    assert result["scale"] == 0.0
    assert np.array_equal(result["quantized"], [0, 0, 0])
    assert np.array_equal(result["dequantized"], [0.0, 0.0, 0.0])


def test_single_large_outlier():
    result = quantize_int8_symmetric(np.array([0.01, 0.02, -0.01, 10.0]))
    assert result["quantized"][3] == 127
    assert abs(result["dequantized"][3] - 10.0) < result["scale"]


def test_already_integer_like_values():
    result = quantize_int8_symmetric(np.array([1, 2, 3, 4, -4]))
    assert result["quantized"][3] == 127  # 4 is the max magnitude
    assert result["quantized"][4] == -127


def test_quantization_error_bounded_by_half_step():
    rng = np.random.default_rng(0)
    x = rng.normal(size=1000)
    result = quantize_int8_symmetric(x)
    error = np.abs(x - result["dequantized"])
    assert np.all(error <= result["scale"] / 2 + 1e-9)


def test_quantized_values_are_integers_within_range():
    result = quantize_int8_symmetric(np.array([100.0, -50.0, 0.0]))
    assert result["quantized"].dtype.kind in ("i", "u")
    assert np.all(result["quantized"] >= -127)
    assert np.all(result["quantized"] <= 127)
