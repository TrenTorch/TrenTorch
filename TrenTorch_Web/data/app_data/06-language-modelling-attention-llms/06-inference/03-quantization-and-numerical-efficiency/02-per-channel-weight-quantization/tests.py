"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

quantize_int8_per_channel = load_solution(__file__).quantize_int8_per_channel
quantize_int8_symmetric = load_solution("inf-quant-int8-symmetric").quantize_int8_symmetric


def test_two_rows_different_magnitudes_get_independent_scales():
    result = quantize_int8_per_channel(np.array([[10.0, -10.0], [0.1, -0.2]]))
    assert not np.isclose(result["scale"][0], result["scale"][1])
    # Each row's max value should quantize to exactly ±127 (its own scale).
    assert 127 in np.abs(result["quantized"][0])
    assert 127 in np.abs(result["quantized"][1])


def test_matches_per_tensor_quantization_row_by_row():
    W = np.array([[10.0, -10.0], [0.1, -0.2], [5.0, 5.0]])
    result = quantize_int8_per_channel(W)
    for row in range(3):
        expected = quantize_int8_symmetric(W[row])
        assert np.array_equal(result["quantized"][row], expected["quantized"])
        assert np.isclose(result["scale"][row], expected["scale"])


def test_all_zero_row():
    result = quantize_int8_per_channel(np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0], [-5.0, 5.0, 0.0]]))
    assert result["scale"][1] == 0.0
    assert np.array_equal(result["quantized"][1], [0, 0, 0])


def test_single_row():
    result = quantize_int8_per_channel(np.array([[3.0, -6.0, 9.0, -12.0]]))
    assert result["quantized"].shape == (1, 4)
    assert result["quantized"][0, 3] == -127  # -12 is the max magnitude


def test_reconstruction_error_bounded_per_row():
    rng = np.random.default_rng(0)
    W = rng.normal(size=(4, 20)) * np.array([[1], [100], [0.01], [10]])
    result = quantize_int8_per_channel(W)
    error = np.abs(W - result["dequantized"])
    for row in range(4):
        assert np.all(error[row] <= result["scale"][row] / 2 + 1e-9)
