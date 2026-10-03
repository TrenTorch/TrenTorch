"""
pytest tests.py
"""

import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
monte_carlo_mean = _module.monte_carlo_mean
estimate_pi = _module.estimate_pi
monte_carlo_integral = _module.monte_carlo_integral
samples_for_precision = _module.samples_for_precision


def _normal_sampler(mean=0.0, std=1.0):
    return lambda rng, n: rng.normal(mean, std, size=n)


# ---- 1-7: Monte Carlo mean ----


def test_1_estimates_the_mean_of_a_normal():
    estimate, _ = monte_carlo_mean(lambda x: x, _normal_sampler(3.0, 2.0), 100_000, np.random.default_rng(0))
    assert abs(estimate - 3.0) < 0.05


def test_2_estimates_the_second_moment():
    estimate, _ = monte_carlo_mean(lambda x: x**2, _normal_sampler(), 200_000, np.random.default_rng(1))
    assert abs(estimate - 1.0) < 0.02


def test_3_standard_error_matches_sigma_over_root_n():
    _, se = monte_carlo_mean(lambda x: x, _normal_sampler(0.0, 2.0), 40_000, np.random.default_rng(2))
    assert abs(se - 2.0 / math.sqrt(40_000)) < 0.002


def test_4_estimate_and_error_match_a_manual_computation():
    rng = np.random.default_rng(3)
    draws = np.random.default_rng(3).normal(size=500)
    estimate, se = monte_carlo_mean(lambda x: np.abs(x), _normal_sampler(), 500, rng)
    assert np.isclose(estimate, np.abs(draws).mean())
    assert np.isclose(se, np.abs(draws).std(ddof=1) / math.sqrt(500))


def test_5_sampler_is_called_exactly_once():
    calls = []

    def sampler(rng, n):
        calls.append(n)
        return rng.random(n)

    monte_carlo_mean(lambda x: x, sampler, 10, np.random.default_rng(4))
    assert calls == [10]


def test_6_error_shrinks_as_the_sample_grows():
    f, s = (lambda x: x), _normal_sampler()
    _, small = monte_carlo_mean(f, s, 100, np.random.default_rng(5))
    _, large = monte_carlo_mean(f, s, 10_000, np.random.default_rng(5))
    assert large < small


def test_7_returns_plain_floats():
    estimate, se = monte_carlo_mean(lambda x: x, _normal_sampler(), 50, np.random.default_rng(6))
    assert isinstance(estimate, float) and isinstance(se, float)


# ---- 8-11: estimating pi ----


def test_8_pi_is_close_with_many_points():
    assert abs(estimate_pi(400_000, np.random.default_rng(0)) - math.pi) < 0.02


def test_9_matches_an_independent_replay_of_the_draws():
    rng = np.random.default_rng(7)
    x = rng.random(1000)
    y = rng.random(1000)
    expected = 4.0 * np.sum(x * x + y * y <= 1.0) / 1000
    assert estimate_pi(1000, np.random.default_rng(7)) == expected


def test_10_estimate_is_a_multiple_of_four_over_n():
    value = estimate_pi(10, np.random.default_rng(8))
    assert np.isclose(value * 10 / 4, round(value * 10 / 4))


def test_11_more_points_give_a_smaller_typical_error():
    small = [abs(estimate_pi(100, np.random.default_rng(s)) - math.pi) for s in range(60)]
    large = [abs(estimate_pi(10_000, np.random.default_rng(s)) - math.pi) for s in range(60)]
    assert np.mean(large) < np.mean(small)


# ---- 12-15: integration ----


def test_12_integral_of_x_squared_over_zero_one():
    value = monte_carlo_integral(lambda x: x**2, 0.0, 1.0, 300_000, np.random.default_rng(0))
    assert abs(value - 1 / 3) < 0.005


def test_13_integral_scales_with_the_interval_length():
    value = monte_carlo_integral(lambda x: np.ones_like(x), 2.0, 7.0, 1000, np.random.default_rng(1))
    assert np.isclose(value, 5.0)


def test_14_integral_of_sine_over_zero_pi_is_two():
    value = monte_carlo_integral(np.sin, 0.0, math.pi, 400_000, np.random.default_rng(2))
    assert abs(value - 2.0) < 0.02


def test_15_matches_an_independent_replay_of_the_draws():
    u = np.random.default_rng(9).uniform(-1.0, 3.0, size=500)
    expected = 4.0 * np.mean(np.exp(u))
    assert np.isclose(monte_carlo_integral(np.exp, -1.0, 3.0, 500, np.random.default_rng(9)), expected)


# ---- 16-19: sample size ----


def test_16_hand_computed_sample_size():
    assert samples_for_precision(2.0, 0.1) == 400


def test_17_rounds_up():
    assert samples_for_precision(1.0, 0.3) == 12  # (1 / 0.3)^2 = 11.1


def test_18_halving_the_error_quadruples_the_samples():
    assert samples_for_precision(3.0, 0.05) == 4 * samples_for_precision(3.0, 0.1)


def test_19_non_positive_target_raises_value_error():
    for bad in (0.0, -0.1):
        with pytest.raises(ValueError):
            samples_for_precision(1.0, bad)
