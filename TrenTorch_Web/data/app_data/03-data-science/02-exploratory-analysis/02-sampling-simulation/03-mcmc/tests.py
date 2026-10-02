"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
metropolis_hastings = _module.metropolis_hastings
burn_in_and_thin = _module.burn_in_and_thin
autocorrelation = _module.autocorrelation
mcmc_effective_sample_size = _module.mcmc_effective_sample_size


def _log_normal(x):
    return -0.5 * x * x  # standard normal without its constant


def _ar1(phi, n=20_000, seed=0):
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + rng.normal()
    return x


# ---- 1-9: Metropolis ----


def test_1_samples_the_standard_normal():
    samples, _ = metropolis_hastings(_log_normal, 0.0, 60_000, 2.4, np.random.default_rng(0))
    kept = burn_in_and_thin(samples, 1000, 1)
    assert abs(kept.mean()) < 0.05 and abs(kept.std() - 1.0) < 0.05


def test_2_works_with_an_unnormalized_target_of_another_shape():
    # density proportional to exp(-x) on x > 0: an exponential with mean 1
    def log_target(x):
        return -x if x > 0 else -np.inf

    samples, _ = metropolis_hastings(log_target, 1.0, 80_000, 1.5, np.random.default_rng(1))
    kept = burn_in_and_thin(samples, 2000, 1)
    assert abs(kept.mean() - 1.0) < 0.1 and kept.min() > 0.0


def test_3_returns_one_sample_per_step_and_a_rate_in_range():
    samples, rate = metropolis_hastings(_log_normal, 0.0, 500, 1.0, np.random.default_rng(2))
    assert samples.shape == (500,) and 0.0 <= rate <= 1.0


def test_4_matches_an_independent_replay_of_the_draws():
    rng = np.random.default_rng(3)
    x, samples, accepted = 0.5, [], 0
    for _ in range(200):
        step = rng.normal()
        u = rng.random()
        proposal = x + 0.8 * step
        if np.log(u) < _log_normal(proposal) - _log_normal(x):
            x = proposal
            accepted += 1
        samples.append(x)
    got, rate = metropolis_hastings(_log_normal, 0.5, 200, 0.8, np.random.default_rng(3))
    np.testing.assert_array_equal(got, samples)
    assert rate == accepted / 200


def test_5_a_rejected_step_repeats_the_previous_sample():
    samples, rate = metropolis_hastings(_log_normal, 0.0, 400, 50.0, np.random.default_rng(4))
    repeats = np.sum(samples[1:] == samples[:-1])
    assert rate < 0.2 and repeats > 250


def test_6_tiny_steps_are_accepted_almost_always_and_barely_move():
    samples, rate = metropolis_hastings(_log_normal, 0.0, 2000, 0.01, np.random.default_rng(5))
    assert rate > 0.95 and samples.std() < 0.5


def test_7_moves_to_higher_density_are_always_accepted():
    # a target that increases to the right: every proposal to the right is accepted
    samples, _ = metropolis_hastings(lambda x: x, 0.0, 300, 1.0, np.random.default_rng(6))
    assert samples[-1] > samples[0]


def test_8_stays_inside_a_bounded_support():
    def log_target(x):
        return 0.0 if 0.0 <= x <= 1.0 else -np.inf

    samples, _ = metropolis_hastings(log_target, 0.5, 5000, 0.4, np.random.default_rng(7))
    assert samples.min() >= 0.0 and samples.max() <= 1.0
    assert abs(samples.mean() - 0.5) < 0.05


def test_9_visits_both_modes_of_a_bimodal_target():
    def log_target(x):
        return np.log(np.exp(-0.5 * (x - 3.0) ** 2) + np.exp(-0.5 * (x + 3.0) ** 2))

    samples, _ = metropolis_hastings(log_target, -3.0, 40_000, 3.0, np.random.default_rng(8))
    assert samples.max() > 2.0 and samples.min() < -2.0


# ---- 10-12: burn-in and thinning ----


def test_10_burn_in_drops_the_first_samples():
    np.testing.assert_array_equal(burn_in_and_thin(np.arange(10.0), 3, 1), np.arange(3.0, 10.0))


def test_11_thinning_keeps_every_kth():
    np.testing.assert_array_equal(burn_in_and_thin(np.arange(10.0), 0, 3), [0.0, 3.0, 6.0, 9.0])


def test_12_returns_a_new_array():
    x = np.arange(5.0)
    result = burn_in_and_thin(x, 0, 1)
    result[0] = 99.0
    assert x[0] == 0.0


# ---- 13-17: autocorrelation ----


def test_13_lag_zero_is_one():
    assert np.isclose(autocorrelation(np.random.default_rng(0).normal(size=100), 0), 1.0)


def test_14_hand_computed_value():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    centered = x - 2.5
    expected = np.sum(centered[:-1] * centered[1:]) / np.sum(centered**2)
    assert np.isclose(autocorrelation(x, 1), expected)
    assert np.isclose(expected, 0.25)


def test_15_ar1_series_has_autocorrelation_phi_to_the_lag():
    x = _ar1(0.8)
    assert abs(autocorrelation(x, 1) - 0.8) < 0.03
    assert abs(autocorrelation(x, 3) - 0.8**3) < 0.04


def test_16_independent_draws_have_near_zero_autocorrelation():
    x = np.random.default_rng(1).normal(size=20_000)
    assert abs(autocorrelation(x, 1)) < 0.03


def test_17_constant_series_gives_zero_not_a_division_error():
    assert autocorrelation(np.ones(10), 2) == 0.0


# ---- 18-22: effective sample size ----


def test_18_independent_draws_are_worth_about_n():
    x = np.random.default_rng(2).normal(size=10_000)
    assert mcmc_effective_sample_size(x, 50) > 0.8 * 10_000


def test_19_ar1_matches_the_theoretical_value():
    x = _ar1(0.9, n=50_000, seed=3)
    theory = len(x) * (1 - 0.9) / (1 + 0.9)
    assert abs(mcmc_effective_sample_size(x, 200) - theory) / theory < 0.3


def test_20_stronger_dependence_means_a_smaller_effective_size():
    a = mcmc_effective_sample_size(_ar1(0.3), 100)
    b = mcmc_effective_sample_size(_ar1(0.9), 100)
    assert b < a


def test_21_result_is_between_one_and_n():
    x = _ar1(0.99, n=500, seed=4)
    ess = mcmc_effective_sample_size(x, 100)
    assert 1.0 <= ess <= 500.0


def test_22_a_good_step_size_beats_a_tiny_one_on_effective_size():
    good, _ = metropolis_hastings(_log_normal, 0.0, 20_000, 2.4, np.random.default_rng(5))
    tiny, _ = metropolis_hastings(_log_normal, 0.0, 20_000, 0.05, np.random.default_rng(5))
    assert mcmc_effective_sample_size(good, 200) > 5 * mcmc_effective_sample_size(tiny, 200)
