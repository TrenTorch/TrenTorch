"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
replace_where = _module.replace_where
clip_to_percentiles = _module.clip_to_percentiles
sign_class = _module.sign_class
bucket_label = _module.bucket_label


def test_replace_where_sets_the_selected_positions():
    a = np.array([5, -2, 7, -1])
    np.testing.assert_array_equal(replace_where(a, a < 0, 0), [5, 0, 7, 0])


def test_replace_where_does_not_change_the_input():
    a = np.array([1, 2, 3])
    replace_where(a, a > 1, 99)
    np.testing.assert_array_equal(a, [1, 2, 3])


def test_replace_where_with_an_all_false_mask_returns_equal_values():
    a = np.array([1.5, 2.5])
    np.testing.assert_array_equal(replace_where(a, np.array([False, False]), 0.0), a)


def test_replace_where_works_on_2d_arrays():
    m = np.array([[1, 2], [3, 4]])
    np.testing.assert_array_equal(replace_where(m, m % 2 == 0, -1), [[1, -1], [3, -1]])


def test_clip_to_percentiles_limits_the_extremes():
    a = np.array([1.0, 2.0, 3.0, 4.0, 100.0])
    out = clip_to_percentiles(a, 0, 80)
    np.testing.assert_allclose(out, np.clip(a, np.percentile(a, 0), np.percentile(a, 80)))
    assert out.max() < 100.0


def test_clip_matches_numpy_on_random_data():
    a = np.random.default_rng(0).normal(size=200)
    lo, hi = np.percentile(a, [5, 95])
    np.testing.assert_allclose(clip_to_percentiles(a, 5, 95), np.clip(a, lo, hi))


def test_clip_values_inside_the_limits_are_unchanged():
    a = np.arange(101.0)
    out = clip_to_percentiles(a, 10, 90)
    np.testing.assert_array_equal(out[10:91], a[10:91])
    assert out.min() == 10.0 and out.max() == 90.0


def test_clip_does_not_change_the_input():
    a = np.array([1.0, 50.0, 2.0])
    before = a.copy()
    clip_to_percentiles(a, 10, 90)
    np.testing.assert_array_equal(a, before)


def test_sign_class():
    np.testing.assert_array_equal(sign_class(np.array([-3.5, 0.0, 2.0, -0.1, 9])), [-1, 0, 1, -1, 1])


def test_sign_class_is_an_integer_array_of_the_same_shape():
    m = np.array([[1, -1], [0, 5]])
    out = sign_class(m)
    assert out.shape == m.shape and out.dtype.kind == "i"


def test_bucket_label_uses_low_mid_high():
    out = bucket_label(np.array([1, 5, 10, 11, 3]), 3, 10)
    assert out.tolist() == ["low", "mid", "high", "high", "mid"]


def test_bucket_label_boundaries():
    out = bucket_label(np.array([2.99, 3.0, 9.99, 10.0]), 3.0, 10.0)
    assert out.tolist() == ["low", "mid", "mid", "high"]
