"""
pytest tests.py
"""

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
skewness = _module.skewness
log1p_transform = _module.log1p_transform
inverse_log1p = _module.inverse_log1p
box_cox = _module.box_cox
best_box_cox_lambda = _module.best_box_cox_lambda


def _lognormal(seed=0, n=5000):
    return np.random.default_rng(seed).lognormal(mean=0.0, sigma=1.0, size=n)


# ---- 1-5: skewness ----


def test_1_hand_computed_skewness():
    # [0, 0, 3]: mean 1, std sqrt(2), z = [-1/sqrt2, -1/sqrt2, 2/sqrt2]
    expected = np.mean(np.array([-1, -1, 2]) ** 3 / 2 ** 1.5)
    assert np.isclose(skewness(np.array([0.0, 0.0, 3.0])), expected)


def test_2_symmetric_sample_has_zero_skewness():
    assert np.isclose(skewness(np.array([1.0, 2.0, 3.0, 4.0, 5.0])), 0.0)


def test_3_sign_follows_the_long_tail():
    assert skewness(_lognormal()) > 1.0
    assert skewness(-_lognormal()) < -1.0


def test_4_constant_sample_gives_zero_without_dividing_by_zero():
    assert skewness(np.full(10, 3.0)) == 0.0


def test_5_skewness_is_scale_and_shift_invariant():
    x = _lognormal(1, 500)
    assert np.isclose(skewness(x), skewness(7.0 * x + 100.0))


# ---- 6-9: log transform ----


def test_6_log1p_matches_numpy_and_handles_zero():
    x = np.array([0.0, 1.0, np.e - 1])
    np.testing.assert_allclose(log1p_transform(x), [0.0, np.log(2.0), 1.0])


def test_7_inverse_round_trips():
    x = _lognormal(2, 200)
    np.testing.assert_allclose(inverse_log1p(log1p_transform(x)), x, rtol=1e-10)


def test_8_negative_values_raise_value_error():
    with pytest.raises(ValueError):
        log1p_transform(np.array([1.0, -0.5]))


def test_9_log1p_reduces_the_skew_of_a_lognormal_sample():
    x = _lognormal(3)
    assert abs(skewness(log1p_transform(x))) < abs(skewness(x))


# ---- 10-14: Box-Cox ----


def test_10_lambda_zero_is_the_logarithm():
    x = np.array([1.0, np.e, np.e**2])
    np.testing.assert_allclose(box_cox(x, 0.0), [0.0, 1.0, 2.0])


def test_11_lambda_one_is_the_identity_minus_one():
    x = np.array([1.0, 2.0, 5.0])
    np.testing.assert_allclose(box_cox(x, 1.0), x - 1.0)


def test_12_hand_computed_square_root_case():
    # lambda = 0.5: (sqrt(x) - 1) / 0.5
    np.testing.assert_allclose(box_cox(np.array([4.0, 9.0]), 0.5), [2.0, 4.0])


def test_13_continuity_near_lambda_zero():
    x = np.array([0.5, 2.0, 10.0])
    np.testing.assert_allclose(box_cox(x, 1e-8), box_cox(x, 0.0), atol=1e-6)


def test_14_non_positive_values_raise_value_error():
    with pytest.raises(ValueError):
        box_cox(np.array([1.0, 0.0]), 0.5)
    with pytest.raises(ValueError):
        box_cox(np.array([-1.0, 2.0]), 0.0)


# ---- 15-18: choosing lambda ----


def test_15_lognormal_data_picks_a_lambda_near_zero():
    best = best_box_cox_lambda(_lognormal(4), [-1.0, -0.5, 0.0, 0.5, 1.0, 2.0])
    assert best == 0.0


def test_16_symmetric_data_prefers_lambda_one_over_zero():
    x = np.random.default_rng(5).normal(loc=50.0, scale=2.0, size=2000)
    best = best_box_cox_lambda(x, [0.0, 0.5, 1.0])
    assert best in (0.5, 1.0)
    assert abs(skewness(box_cox(x, best))) <= abs(skewness(box_cox(x, 0.0))) + 1e-9


def test_17_returns_one_of_the_candidates_and_breaks_ties_early():
    x = np.array([1.0, 2.0, 3.0])
    assert best_box_cox_lambda(x, [1.0, 1.0]) == 1.0
    assert best_box_cox_lambda(x, [2.0, 0.5, 1.0]) in (2.0, 0.5, 1.0)


def test_18_input_is_not_modified():
    x = _lognormal(6, 100)
    original = x.copy()
    best_box_cox_lambda(x, [0.0, 0.5])
    log1p_transform(x)
    np.testing.assert_array_equal(x, original)
