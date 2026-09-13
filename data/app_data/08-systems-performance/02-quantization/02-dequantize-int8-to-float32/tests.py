"""
pytest data/app_data/08-systems-performance/02-quantization/02-dequantize-int8-to-float32/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/02-quantization/{Path(__file__).resolve().parent.name}")
dequantize = _module.dequantize
quantization_error = _module.quantization_error
quantize = load_solution("08-systems-performance/02-quantization/01-quantize-float32-to-int8").quantize


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_dequantize_matches_hand_computation():
    q = np.array([-128, 0, 127], dtype=np.int8)
    result = dequantize(q, scale=2.0, zero_point=0)
    assert np.allclose(result, [-256.0, 0.0, 254.0])


def test_02_dequantize_reverses_the_zero_point_shift():
    q = np.array([21], dtype=np.int8)  # zero_point itself maps to float 0.0
    result = dequantize(q, scale=0.5, zero_point=21)
    assert np.isclose(result[0], 0.0)


# --- Shape / general-case coverage -----------------------------------


def test_03_round_trip_through_quantize_stays_close_to_the_original():
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0, 1.5])
    q, scale, zero_point = quantize(x)
    reconstructed = dequantize(q, scale, zero_point)
    assert np.allclose(reconstructed, x, atol=0.05)


def test_04_quantization_error_is_small_relative_to_the_datas_own_range():
    rng = np.random.default_rng(0)
    x = rng.normal(size=100)
    q, scale, zero_point = quantize(x)
    error = quantization_error(x, q, scale, zero_point)
    data_range = x.max() - x.min()
    assert error < data_range * 0.01  # well under 1% of the full range


# --- Parameter handling -------------------------------------------------


def test_05_larger_scale_amplifies_the_same_integer_rounding_gap():
    # In both cases q=0 is the nearest integer bin, but the true value
    # sits 0.4 bins away from it -- a larger scale turns that same
    # fractional-bin gap into a larger absolute float error.
    q = np.array([0], dtype=np.int8)
    small_scale_error = quantization_error(np.array([0.04]), q, scale=0.1, zero_point=0)
    large_scale_error = quantization_error(np.array([0.4]), q, scale=1.0, zero_point=0)
    assert large_scale_error > small_scale_error
    assert np.isclose(small_scale_error, 0.04)
    assert np.isclose(large_scale_error, 0.4)


# --- Edge cases ---------------------------------------------------------


def test_06_dequantize_a_single_element_array():
    q = np.array([50], dtype=np.int8)
    result = dequantize(q, scale=0.1, zero_point=0)
    assert result.shape == (1,)
    assert np.isclose(result[0], 5.0)


def test_07_zero_error_when_reconstruction_is_exact():
    x = np.array([0.0, 2.0, -2.0])
    q = np.array([0, 1, -1], dtype=np.int8)
    error = quantization_error(x, q, scale=2.0, zero_point=0)
    assert np.isclose(error, 0.0)


# --- Array hygiene ------------------------------------------------------


def test_08_does_not_mutate_its_inputs():
    q = np.array([-10, 0, 10], dtype=np.int8)
    q_copy = q.copy()
    dequantize(q, scale=1.5, zero_point=0)
    assert np.array_equal(q, q_copy)


def test_09_subtracting_zero_point_does_not_wrap_around_int8():
    # Directly targets a mutant that subtracts zero_point from q BEFORE
    # casting to float: int8 arithmetic wraps around on overflow, e.g.
    # (-128 - 100) as int8 wraps to a small positive number instead of
    # the correct large negative one.
    q = np.array([-128], dtype=np.int8)
    result = dequantize(q, scale=1.0, zero_point=100)
    assert np.isclose(result[0], -228.0)


# --- Independent correctness oracle -----------------------------------


def test_10_matches_real_pytorch_dequantize_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   torch.manual_seed(0)
    #   x = torch.randn(8) * 3
    #   qt = torch.quantize_per_tensor(x, scale=0.04376235288732192, zero_point=21, dtype=torch.qint8)
    #   qt.dequantize()  # baked below
    #
    # This test needs no torch installed to run.
    q = np.array([127, 1, -128, 60, -53, -75, 49, 78], dtype=np.int8)
    scale = 0.04376235288732192
    zero_point = 21
    expected = np.array(
        [4.6391, -0.8752, -6.5206, 1.7067, -3.2384, -4.2012, 1.2253, 2.4944], dtype=np.float32
    )
    result = dequantize(q, scale, zero_point)
    assert np.allclose(result, expected, atol=1e-3)
