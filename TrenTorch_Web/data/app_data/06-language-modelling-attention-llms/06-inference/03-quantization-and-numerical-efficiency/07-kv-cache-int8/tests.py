"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
quantize_kv = _module.quantize_kv
dequantize_kv = _module.dequantize_kv


def test_1_hand_computed():
    kv = np.array([[[127.0, -63.5, 0.0]]])
    q, scale = quantize_kv(kv)
    assert np.isclose(scale[0, 0], 1.0)
    assert q.tolist() == [[[127, -64, 0]]]  # -63.5 rounds half to even -> -64


def test_2_dtype_and_shapes():
    kv = np.random.RandomState(0).randn(5, 3, 8)
    q, scale = quantize_kv(kv)
    assert q.dtype == np.int8 and q.shape == (5, 3, 8) and scale.shape == (5, 3)


def test_3_largest_element_maps_to_127():
    kv = np.random.RandomState(1).randn(4, 2, 16)
    q, _ = quantize_kv(kv)
    assert np.all(np.abs(q).max(axis=-1) == 127)


def test_4_error_is_at_most_half_a_step():
    kv = np.random.RandomState(2).randn(6, 4, 32) * 5
    q, scale = quantize_kv(kv)
    err = np.abs(dequantize_kv(q, scale) - kv)
    assert (err <= scale[..., None] / 2 + 1e-9).all()


def test_5_per_vector_scale_isolates_outliers():
    kv = np.ones((2, 1, 4))
    kv[0] *= 1000.0
    q, scale = quantize_kv(kv)
    assert np.allclose(dequantize_kv(q, scale)[1], 1.0)


def test_6_zero_vectors_are_safe():
    q, scale = quantize_kv(np.zeros((2, 2, 4)))
    assert np.all(dequantize_kv(q, scale) == 0.0) and np.all(np.isfinite(scale))


def test_7_input_untouched_and_dequantized_is_float():
    kv = np.random.RandomState(3).randn(3, 2, 8)
    snap = kv.copy()
    q, scale = quantize_kv(kv)
    assert np.array_equal(kv, snap) and np.issubdtype(dequantize_kv(q, scale).dtype, np.floating)
