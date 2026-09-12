"""
pytest data/app_data/00-math-and-statistics/03-probability/08-map-estimation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
negative_log_posterior_normal = _module.negative_log_posterior_normal
map_estimate_normal_mean = _module.map_estimate_normal_mean


def test_map_estimate_with_uninformative_prior_approaches_sample_mean():
    rng = np.random.default_rng(0)
    x = rng.normal(5.0, 2.0, size=20)
    result = map_estimate_normal_mean(x, data_std=2.0, prior_mean=0.0, prior_std=1e6)
    assert np.isclose(result, np.mean(x), atol=1e-3)


def test_map_estimate_with_extremely_confident_prior_approaches_prior_mean():
    rng = np.random.default_rng(1)
    x = rng.normal(5.0, 2.0, size=20)
    result = map_estimate_normal_mean(x, data_std=2.0, prior_mean=100.0, prior_std=1e-6)
    assert np.isclose(result, 100.0, atol=1e-3)


def test_map_estimate_is_between_sample_mean_and_prior_mean():
    x = np.array([10.0, 12.0, 11.0, 13.0, 9.0])
    sample_mean = np.mean(x)
    prior_mean = 0.0
    result = map_estimate_normal_mean(x, data_std=2.0, prior_mean=prior_mean, prior_std=2.0)
    assert min(sample_mean, prior_mean) <= result <= max(sample_mean, prior_mean)


def test_map_estimate_matches_hand_computation():
    # n=4, sample_mean=10, data_std=2 -> data_precision = 4/4 = 1
    # prior_mean=0, prior_std=1 -> prior_precision = 1
    # map = (1*10 + 1*0) / (1+1) = 5.0
    x = np.array([8.0, 9.0, 11.0, 12.0])  # mean = 10
    result = map_estimate_normal_mean(x, data_std=2.0, prior_mean=0.0, prior_std=1.0)
    assert np.isclose(result, 5.0)


def test_map_estimate_minimizes_negative_log_posterior_vs_nearby_candidates():
    rng = np.random.default_rng(2)
    x = rng.normal(5.0, 2.0, size=30)
    data_std, prior_mean, prior_std = 2.0, 3.0, 1.0
    best = map_estimate_normal_mean(x, data_std, prior_mean, prior_std)
    best_value = negative_log_posterior_normal(best, x, data_std, prior_mean, prior_std)

    for delta in [-0.3, -0.1, 0.1, 0.3]:
        candidate_value = negative_log_posterior_normal(
            best + delta, x, data_std, prior_mean, prior_std
        )
        assert candidate_value >= best_value - 1e-6


def test_more_data_shifts_map_estimate_toward_sample_mean():
    # As n grows (with everything else fixed), data_precision grows,
    # pulling the MAP estimate away from the prior and toward the
    # sample mean.
    rng = np.random.default_rng(3)
    prior_mean, prior_std, data_std = 0.0, 1.0, 2.0
    true_mean = 10.0

    small_sample = rng.normal(true_mean, data_std, size=3)
    large_sample = rng.normal(true_mean, data_std, size=10_000)

    map_small = map_estimate_normal_mean(small_sample, data_std, prior_mean, prior_std)
    map_large = map_estimate_normal_mean(large_sample, data_std, prior_mean, prior_std)

    assert abs(map_large - true_mean) < abs(map_small - prior_mean)
    assert np.isclose(map_large, true_mean, atol=0.5)


def test_map_estimate_uses_precision_weighting_not_a_plain_average():
    # Directly targets a mutant that computes a plain, unweighted average
    # of sample_mean and prior_mean (ignoring precision entirely). With
    # a much more confident prior than the data, the correct MAP should
    # sit far closer to the prior mean than a 50/50 average would.
    x = np.array([100.0, 102.0, 98.0, 101.0, 99.0])  # sample mean = 100
    result = map_estimate_normal_mean(x, data_std=10.0, prior_mean=0.0, prior_std=0.1)
    naive_average = (np.mean(x) + 0.0) / 2.0  # would be 50.0
    assert not np.isclose(result, naive_average, atol=5.0)
    assert result < 10.0  # should sit very close to the confident prior (0.0)
