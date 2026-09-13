"""
pytest data/app_data/08-systems-performance/02-quantization/01-quantize-float32-to-int8/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/02-quantization/{Path(__file__).resolve().parent.name}")
compute_scale_zero_point = _module.compute_scale_zero_point
quantize = _module.quantize


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_quantized_dtype_is_int8():
    x = np.array([-1.0, 0.0, 1.0])
    q, _, _ = quantize(x)
    assert q.dtype == np.int8


def test_02_min_and_max_map_to_the_int8_extremes():
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    q, _, _ = quantize(x)
    assert q.min() == -128
    assert q.max() == 127


# --- Shape / general-case coverage -----------------------------------


def test_03_scale_matches_hand_computation():
    x = np.array([0.0, 255.0])  # range of 255 over 255 integer steps -> scale 1.0
    scale, _ = compute_scale_zero_point(x)
    assert np.isclose(scale, 1.0)


def test_04_zero_point_matches_hand_computation():
    # x's own minimum (0.0) should map to qmin (-128) exactly when scale=1.
    x = np.array([0.0, 255.0])
    scale, zero_point = compute_scale_zero_point(x)
    assert zero_point == -128


def test_05_all_quantized_values_stay_within_int8_range():
    rng = np.random.default_rng(0)
    x = rng.normal(scale=100.0, size=50)
    q, _, _ = quantize(x)
    assert np.all(q >= -128) and np.all(q <= 127)


# --- Parameter handling -------------------------------------------------


def test_06_larger_range_gives_a_larger_scale():
    narrow = np.array([-1.0, 1.0])
    wide = np.array([-100.0, 100.0])
    narrow_scale, _ = compute_scale_zero_point(narrow)
    wide_scale, _ = compute_scale_zero_point(wide)
    assert wide_scale > narrow_scale


# --- Edge cases ---------------------------------------------------------


def test_07_constant_array_does_not_divide_by_zero():
    x = np.full(5, 3.0)
    scale, zero_point = compute_scale_zero_point(x)
    assert scale > 0.0
    assert np.isfinite(scale)
    q, _, _ = quantize(x)
    assert np.all(np.isfinite(q.astype(np.float64)))


def test_08_single_element_array_works():
    x = np.array([7.5])
    q, scale, zero_point = quantize(x)
    assert q.shape == (1,)
    assert np.isfinite(scale)


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_input():
    x = np.array([-1.0, 0.0, 1.0])
    x_copy = x.copy()
    quantize(x)
    assert np.array_equal(x, x_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_matches_real_pytorch_quantize_per_tensor_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   torch.manual_seed(0)
    #   x = torch.randn(8) * 3
    #   scale, zero_point = <this exercise's own compute_scale_zero_point>(x.numpy())
    #   q = torch.quantize_per_tensor(x, scale=scale, zero_point=zero_point, dtype=torch.qint8)
    #   q.int_repr()  # baked below -- matches this exercise's own quantize(x) exactly,
    #                 # confirming the affine quantization formula matches PyTorch's own
    #
    # This test needs no torch installed to run.
    x = np.array(
        [4.6230, -0.8803, -6.5364, 1.7053, -3.2536, -4.1958, 1.2100, 2.5141], dtype=np.float32
    )
    expected_q = np.array([127, 1, -128, 60, -53, -75, 49, 78], dtype=np.int8)

    q, scale, zero_point = quantize(x)
    assert np.array_equal(q, expected_q)
    assert np.isclose(scale, 0.04376235288732192, atol=1e-6)
    assert zero_point == 21
