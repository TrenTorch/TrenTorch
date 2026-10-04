"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
nf4_quantize = _module.nf4_quantize
nf4_dequantize = _module.nf4_dequantize
LEVELS = _module.NF4_LEVELS


def test_1_table_has_16_sorted_levels_with_exact_zero():
    assert len(LEVELS) == 16 and np.all(np.diff(LEVELS) > 0)
    assert LEVELS[0] == -1.0 and LEVELS[-1] == 1.0 and 0.0 in LEVELS


def test_2_values_on_the_grid_round_trip_exactly():
    w = np.concatenate([LEVELS * 2.0, LEVELS * 0.5])
    codes, scales = nf4_quantize(w, 16)
    assert np.allclose(scales, [2.0, 0.5])
    assert np.array_equal(codes[:16], np.arange(16))
    assert np.allclose(nf4_dequantize(codes, scales, 16), w)


def test_3_absmax_element_is_reproduced_exactly():
    w = np.array([0.3, -1.7, 0.2, 0.9])
    codes, scales = nf4_quantize(w, 4)
    assert np.isclose(nf4_dequantize(codes, scales, 4)[1], -1.7)


def test_4_codes_are_in_range_and_integer():
    w = np.random.RandomState(0).randn(128)
    codes, _ = nf4_quantize(w, 64)
    assert codes.min() >= 0 and codes.max() <= 15 and np.issubdtype(codes.dtype, np.integer)


def test_5_all_zero_block_is_safe():
    codes, scales = nf4_quantize(np.zeros(8), 4)
    assert np.allclose(nf4_dequantize(codes, scales, 4), 0.0)


def test_6_error_is_bounded_by_half_the_widest_gap_times_scale():
    w = np.random.RandomState(1).randn(256)
    codes, scales = nf4_quantize(w, 64)
    err = np.abs(nf4_dequantize(codes, scales, 64) - w).reshape(-1, 64)
    widest = np.diff(LEVELS).max()
    assert (err <= widest / 2 * scales[:, None] + 1e-9).all()


def test_7_beats_evenly_spaced_4bit_on_normal_weights_and_input_untouched():
    w = np.random.RandomState(2).randn(4096)
    snap = w.copy()
    codes, scales = nf4_quantize(w, 64)
    nf4_err = np.mean((nf4_dequantize(codes, scales, 64) - w) ** 2)
    blocks = w.reshape(-1, 64)
    s = np.abs(blocks).max(axis=1, keepdims=True)
    uni = np.round(blocks / s * 7) / 7 * s
    assert nf4_err < np.mean((uni.reshape(-1) - w) ** 2)
    assert np.array_equal(w, snap)
