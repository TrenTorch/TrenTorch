"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
importance_estimate = _module.importance_estimate
self_normalized_estimate = _module.self_normalized_estimate
effective_sample_size = _module.effective_sample_size


def _normal_pdf(mean, std):
    return lambda x: np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * math.sqrt(2 * math.pi))


# ---- 1-7: plain estimator ----


def test_1_same_proposal_as_target_gives_the_plain_mean():
    draws = np.random.default_rng(0).normal(size=1000)
    p = _normal_pdf(0.0, 1.0)
    assert np.isclose(importance_estimate(lambda x: x, p, p, draws), draws.mean())


def test_2_recovers_the_mean_of_the_target_from_a_shifted_proposal():
    draws = np.random.default_rng(1).normal(loc=2.0, scale=2.0, size=200_000)
    estimate = importance_estimate(lambda x: x, _normal_pdf(0.0, 1.0), _normal_pdf(2.0, 2.0), draws)
    assert abs(estimate - 0.0) < 0.03


def test_3_estimates_a_rare_event_probability():
    # P(Z > 4) is about 3.17e-5; plain Monte Carlo with 20k draws would see 0 hits
    draws = np.random.default_rng(2).normal(loc=4.0, scale=1.0, size=20_000)
    estimate = importance_estimate(lambda x: (x > 4.0).astype(float), _normal_pdf(0.0, 1.0), _normal_pdf(4.0, 1.0), draws)
    assert abs(estimate - 3.167e-5) / 3.167e-5 < 0.1


def test_4_matches_a_hand_computed_weighting():
    draws = np.array([1.0, 2.0])
    p = lambda x: np.array([0.5, 0.25])
    q = lambda x: np.array([0.25, 0.5])
    # weights [2, 0.5]; f = x -> (1*2 + 2*0.5) / 2 = 1.5
    assert np.isclose(importance_estimate(lambda x: x, p, q, draws), 1.5)


def test_5_estimate_of_a_constant_one_is_the_mean_weight():
    draws = np.random.default_rng(3).normal(scale=1.5, size=50_000)
    estimate = importance_estimate(lambda x: np.ones_like(x), _normal_pdf(0.0, 1.0), _normal_pdf(0.0, 1.5), draws)
    assert abs(estimate - 1.0) < 0.02


def test_6_returns_a_plain_float():
    draws = np.array([0.1, 0.2, 0.3])
    value = importance_estimate(lambda x: x, _normal_pdf(0.0, 1.0), _normal_pdf(0.0, 2.0), draws)
    assert isinstance(value, float)


def test_7_inputs_are_not_modified():
    draws = np.random.default_rng(4).normal(size=20)
    original = draws.copy()
    importance_estimate(lambda x: x**2, _normal_pdf(0.0, 1.0), _normal_pdf(0.0, 2.0), draws)
    np.testing.assert_array_equal(draws, original)


# ---- 8-12: self-normalized estimator ----


def test_8_works_with_an_unnormalized_target():
    draws = np.random.default_rng(5).normal(loc=1.0, scale=3.0, size=200_000)
    unnormalized = lambda x: np.exp(-0.5 * x**2)  # standard normal without its constant
    estimate = self_normalized_estimate(lambda x: x**2, unnormalized, _normal_pdf(1.0, 3.0), draws)
    assert abs(estimate - 1.0) < 0.05


def test_9_unchanged_when_the_target_is_scaled_by_a_constant():
    draws = np.random.default_rng(6).normal(size=500)
    p, q = _normal_pdf(0.5, 1.0), _normal_pdf(0.0, 1.5)
    a = self_normalized_estimate(lambda x: x, p, q, draws)
    b = self_normalized_estimate(lambda x: x, lambda x: 37.0 * p(x), q, draws)
    assert np.isclose(a, b)


def test_10_the_plain_estimator_is_not_scale_invariant():
    draws = np.random.default_rng(7).normal(size=500)
    p, q = _normal_pdf(0.5, 1.0), _normal_pdf(0.0, 1.5)
    a = importance_estimate(lambda x: x, p, q, draws)
    b = importance_estimate(lambda x: x, lambda x: 2.0 * p(x), q, draws)
    assert not np.isclose(a, b)


def test_11_hand_computed_self_normalized_case():
    draws = np.array([1.0, 2.0])
    p = lambda x: np.array([0.5, 0.25])
    q = lambda x: np.array([0.25, 0.5])
    # weights [2, 0.5]: (1*2 + 2*0.5) / (2 + 0.5) = 1.2
    assert np.isclose(self_normalized_estimate(lambda x: x, p, q, draws), 1.2)


def test_12_estimate_of_a_constant_is_that_constant():
    draws = np.random.default_rng(8).normal(size=100)
    value = self_normalized_estimate(lambda x: np.full_like(x, 4.5), _normal_pdf(0.0, 1.0), _normal_pdf(0.0, 2.0), draws)
    assert np.isclose(value, 4.5)


# ---- 13-17: effective sample size ----


def test_13_equal_weights_give_the_full_sample_size():
    assert np.isclose(effective_sample_size(np.ones(50)), 50.0)


def test_14_one_dominant_weight_gives_about_one():
    weights = np.array([1000.0] + [0.001] * 99)
    assert effective_sample_size(weights) < 1.01


def test_15_hand_computed_case():
    assert np.isclose(effective_sample_size(np.array([1.0, 3.0])), 16.0 / 10.0)


def test_16_scale_of_the_weights_does_not_matter():
    w = np.random.default_rng(9).random(30)
    assert np.isclose(effective_sample_size(w), effective_sample_size(100.0 * w))


def test_17_bad_proposal_has_lower_effective_size_than_a_good_one():
    rng = np.random.default_rng(10)
    p = _normal_pdf(0.0, 1.0)
    good = rng.normal(0.0, 1.5, size=5000)
    bad = rng.normal(3.0, 1.0, size=5000)
    ess_good = effective_sample_size(p(good) / _normal_pdf(0.0, 1.5)(good))
    ess_bad = effective_sample_size(p(bad) / _normal_pdf(3.0, 1.0)(bad))
    assert ess_bad < ess_good
