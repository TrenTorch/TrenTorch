"""
pytest data/app_data/00-math-and-statistics/03-probability/07-maximum-likelihood-estimation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
negative_log_likelihood_normal = _module.negative_log_likelihood_normal
mle_normal_mean = _module.mle_normal_mean
mle_normal_std = _module.mle_normal_std


def test_mle_normal_mean_matches_hand_computation():
    x = np.array([2.0, 4.0, 6.0])
    assert np.isclose(mle_normal_mean(x), 4.0)


def test_mle_normal_std_matches_hand_computation():
    # x = [2, 4, 6], mean=4, deviations^2 = [4, 0, 4], mean=8/3, sqrt(8/3)
    x = np.array([2.0, 4.0, 6.0])
    assert np.isclose(mle_normal_std(x), np.sqrt(8.0 / 3.0))


def test_mle_normal_std_uses_biased_n_divisor_not_n_minus_1():
    # Directly checks the biased-vs-unbiased distinction Theory names:
    # MLE std divides by n, matching np.std's default (ddof=0), not the
    # np.std(x, ddof=1) unbiased version.
    rng = np.random.default_rng(0)
    x = rng.normal(5.0, 2.0, size=50)
    assert np.isclose(mle_normal_std(x), np.std(x, ddof=0))
    assert not np.isclose(mle_normal_std(x), np.std(x, ddof=1))


def test_negative_log_likelihood_matches_hand_computation():
    x = np.array([0.0])
    # normal_pdf(0, mean=0, std=1) = 1/sqrt(2*pi)
    expected = -np.log(1.0 / np.sqrt(2.0 * np.pi))
    assert np.isclose(negative_log_likelihood_normal(x, mean=0.0, std=1.0), expected, atol=1e-6)


def test_mle_estimates_minimize_negative_log_likelihood_vs_nearby_candidates():
    # The central claim of MLE: the closed-form estimate should beat
    # (produce lower NLL than) any nearby perturbation of either parameter.
    rng = np.random.default_rng(1)
    x = rng.normal(5.0, 2.0, size=200)
    mean_hat = mle_normal_mean(x)
    std_hat = mle_normal_std(x)
    best_nll = negative_log_likelihood_normal(x, mean_hat, std_hat)

    for delta in [-0.5, -0.1, 0.1, 0.5]:
        assert negative_log_likelihood_normal(x, mean_hat + delta, std_hat) >= best_nll - 1e-6
    for delta in [-0.3, -0.1, 0.1, 0.3]:
        assert negative_log_likelihood_normal(x, mean_hat, std_hat + delta) >= best_nll - 1e-6


def test_mle_normal_mean_recovers_true_mean_on_large_sample():
    rng = np.random.default_rng(2)
    x = rng.normal(10.0, 1.0, size=100_000)
    assert np.isclose(mle_normal_mean(x), 10.0, atol=0.05)


def test_mle_normal_std_recovers_true_std_on_large_sample():
    rng = np.random.default_rng(3)
    x = rng.normal(0.0, 3.0, size=100_000)
    assert np.isclose(mle_normal_std(x), 3.0, atol=0.05)


def test_negative_log_likelihood_uses_log_sum_not_negative_log_of_product():
    # Directly targets a mutant that computes -log(product-of-densities)
    # via an explicit product (which underflows to 0 for many samples,
    # making log(-inf) or nan) instead of summing logs. With enough
    # samples, the product-based approach breaks; the log-sum approach
    # must not.
    rng = np.random.default_rng(4)
    x = rng.normal(0.0, 1.0, size=2000)
    result = negative_log_likelihood_normal(x, mean=0.0, std=1.0)
    assert np.isfinite(result)
