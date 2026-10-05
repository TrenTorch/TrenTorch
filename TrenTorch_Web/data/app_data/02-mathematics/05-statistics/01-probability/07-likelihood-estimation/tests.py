"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
normal_pdf = _module.normal_pdf
joint_density = _module.joint_density
likelihood_curve = _module.likelihood_curve
negative_log_likelihood_normal = _module.negative_log_likelihood_normal
mle_normal_mean = _module.mle_normal_mean
mle_normal_std = _module.mle_normal_std
negative_log_posterior_normal = _module.negative_log_posterior_normal
map_estimate_normal_mean = _module.map_estimate_normal_mean


def test_normal_pdf_matches_known_oracle_values():
    # generated once, offline, via scipy.stats.norm.pdf
    x = np.array([1.0, 2.0, 3.0])
    expected = np.array([0.24197072, 0.39894228, 0.24197072])
    assert np.allclose(normal_pdf(x, mean=2.0, std=1.0), expected, atol=1e-6)


def test_normal_pdf_peaks_at_the_mean():
    x = np.linspace(-5.0, 5.0, 101)
    densities = normal_pdf(x, mean=0.0, std=1.0)
    assert np.isclose(x[np.argmax(densities)], 0.0, atol=0.1)


def test_normal_pdf_is_never_negative():
    x = np.array([-100.0, -1.0, 0.0, 1.0, 100.0])
    assert np.all(normal_pdf(x, mean=0.0, std=1.0) >= 0.0)


def test_joint_density_is_product_of_individual_densities():
    x_values = np.array([1.0, 2.0, 3.0])
    expected = np.prod([normal_pdf(np.array([v]), 2.0, 1.0)[0] for v in x_values])
    assert np.isclose(joint_density(x_values, mean=2.0, std=1.0), expected)


def test_likelihood_curve_returns_one_value_per_candidate_mean():
    x_values = np.array([1.0, 2.0, 3.0])
    candidates = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    result = likelihood_curve(x_values, candidates, std=1.0)
    assert result.shape == (5,)


def test_likelihood_curve_peaks_at_the_sample_mean():
    # The core MLE fact this question sets up: the likelihood curve for
    # a Normal distribution's mean peaks exactly at the sample mean.
    x_values = np.array([2.0, 4.0, 6.0])  # sample mean = 4.0
    candidates = np.linspace(0.0, 8.0, 81)
    result = likelihood_curve(x_values, candidates, std=1.0)
    best_mean = candidates[np.argmax(result)]
    assert np.isclose(best_mean, 4.0, atol=0.15)


def test_likelihood_curve_is_not_confused_with_summing_instead_of_multiplying():
    # Directly targets a mutant that sums individual densities instead
    # of multiplying them (treating the joint density like a probability
    # of "any" observation rather than "all" observations together).
    # For 3 independent observations, product and sum give very
    # different numbers except in degenerate cases.
    x_values = np.array([1.0, 2.0, 3.0])
    correct = joint_density(x_values, mean=2.0, std=1.0)
    individual_densities = normal_pdf(x_values, mean=2.0, std=1.0)
    wrong_sum_version = np.sum(individual_densities)
    assert not np.isclose(correct, wrong_sum_version)
    assert np.isclose(correct, np.prod(individual_densities))


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
