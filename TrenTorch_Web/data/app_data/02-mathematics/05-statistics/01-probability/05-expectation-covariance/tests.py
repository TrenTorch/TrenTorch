"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
expectation = _module.expectation
variance = _module.variance
covariance = _module.covariance
pmf_covariance = _module.pmf_covariance
sample_mean = _module.sample_mean
sample_variance = _module.sample_variance
correlation = _module.correlation


# ---- 1-2: basic correctness ----


def test_1_expectation_of_a_fair_die():
    result = expectation([1, 2, 3, 4, 5, 6], [1 / 6] * 6)
    assert np.isclose(result, 3.5)


def test_2_variance_of_a_fair_coin_valued_0_and_1():
    # Var = E[X^2] - E[X]^2 = 0.5 - 0.25 = 0.25
    result = variance([0, 1], [0.5, 0.5])
    assert np.isclose(result, 0.25)


# ---- shape / general-case coverage ----


def test_3_variance_of_a_constant_random_variable_is_zero():
    result = variance([7, 7, 7], [0.2, 0.3, 0.5])
    assert np.isclose(result, 0.0, atol=1e-9)


def test_4_covariance_of_independent_variables_is_zero():
    marginal_x = np.array([0.3, 0.7])
    marginal_y = np.array([0.4, 0.6])
    joint = np.outer(marginal_x, marginal_y)
    result = pmf_covariance([0, 1], [0, 1], joint)
    assert np.isclose(result, 0.0, atol=1e-9)


def test_5_covariance_of_perfectly_correlated_variables_equals_the_variance():
    # X and Y always equal (0,0) or (1,1) with equal probability.
    joint = np.array([[0.5, 0.0], [0.0, 0.5]])
    x_values = [0, 1]
    y_values = [0, 1]
    cov = pmf_covariance(x_values, y_values, joint)
    var_x = variance(x_values, joint.sum(axis=1))
    assert np.isclose(cov, var_x)


# ---- edge cases ----


def test_6_expectation_of_a_single_outcome():
    result = expectation([42], [1.0])
    assert np.isclose(result, 42.0)


def test_7_covariance_of_negatively_correlated_variables_is_negative():
    # X and Y always take opposite values: (0,1) or (1,0).
    joint = np.array([[0.0, 0.5], [0.5, 0.0]])
    result = pmf_covariance([0, 1], [0, 1], joint)
    assert result < 0


# ---- mutation-catching ----


def test_8_variance_uses_squared_deviation_not_absolute_deviation():
    # A wrong implementation using |x - mean| instead of (x - mean)**2
    # would give a different value for this asymmetric distribution.
    values = [1, 10]
    probabilities = [0.9, 0.1]
    mean = expectation(values, probabilities)  # 1.9
    expected_variance = 0.9 * (1 - mean) ** 2 + 0.1 * (10 - mean) ** 2
    result = variance(values, probabilities)
    assert np.isclose(result, expected_variance)


def test_9_covariance_centers_both_variables_not_just_one():
    # A wrong implementation forgetting to subtract mean_y (using raw y
    # instead of y - mean_y) would give a different, generally nonzero,
    # result even for independent variables.
    marginal_x = np.array([0.5, 0.5])
    marginal_y = np.array([0.5, 0.5])
    joint = np.outer(marginal_x, marginal_y)
    result = pmf_covariance([0, 1], [10, 20], joint)
    assert np.isclose(result, 0.0, atol=1e-9)


# ---- independent oracle ----


def test_10_matches_a_hand_computed_reference_case():
    values = [2, 4, 6]
    probabilities = [0.2, 0.5, 0.3]
    mean = expectation(values, probabilities)
    assert np.isclose(mean, 4.2)
    expected_variance = sum(p * (v - mean) ** 2 for v, p in zip(values, probabilities))
    assert np.isclose(variance(values, probabilities), expected_variance)


def test_sample_mean_matches_hand_computation():
    x = np.array([2.0, 4.0, 6.0, 8.0])
    assert np.isclose(sample_mean(x), 5.0)


def test_sample_mean_of_constant_array_is_that_constant():
    assert np.isclose(sample_mean(np.array([7.0, 7.0, 7.0])), 7.0)


def test_sample_variance_of_constant_array_is_zero():
    assert np.isclose(sample_variance(np.array([3.0, 3.0, 3.0])), 0.0)


def test_sample_variance_ddof0_matches_hand_computation():
    x = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    # population variance (ddof=0): mean=5, sum((x-5)^2)=32, /8 = 4.0
    assert np.isclose(sample_variance(x, ddof=0), 4.0)


def test_sample_variance_ddof1_is_larger_than_ddof0():
    # Bessel's correction (n-1) always produces a larger-or-equal value
    # than the plain (n) divisor, for n > 1.
    x = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    biased = sample_variance(x, ddof=0)
    unbiased = sample_variance(x, ddof=1)
    assert unbiased > biased


def test_sample_variance_ddof1_matches_hand_computation():
    x = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    # unbiased variance (ddof=1): sum((x-5)^2)=32, /7 ~= 4.5714
    assert np.isclose(sample_variance(x, ddof=1), 32.0 / 7.0)


def test_sample_variance_respects_ddof_parameter_not_hardcoded():
    # Directly targets a mutant that ignores the `ddof` argument and
    # always computes the population (ddof=0) variance: for this data,
    # ddof=0 and ddof=1 give clearly different numbers.
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result_ddof0 = sample_variance(x, ddof=0)
    result_ddof1 = sample_variance(x, ddof=1)
    assert not np.isclose(result_ddof0, result_ddof1)
    assert np.isclose(result_ddof0, 2.0)
    assert np.isclose(result_ddof1, 2.5)


def test_sample_mean_and_variance_return_plain_floats():
    x = np.array([1.0, 2.0, 3.0])
    assert isinstance(sample_mean(x), float)
    assert isinstance(sample_variance(x), float)


def test_covariance_matches_hand_computation():
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([2.0, 4.0, 6.0])
    # mean_x=2, mean_y=4, deviations: [-1,0,1], [-2,0,2]
    # products: [2, 0, 2], sum=4, /3 (ddof=0) = 1.333...
    assert np.isclose(covariance(x, y, ddof=0), 4.0 / 3.0)


def test_covariance_of_variable_with_itself_equals_variance():
    x = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    assert np.isclose(covariance(x, x, ddof=0), np.var(x, ddof=0))
    assert np.isclose(covariance(x, x, ddof=1), np.var(x, ddof=1))


def test_covariance_matches_numpy_cov():
    rng = np.random.default_rng(0)
    x = rng.normal(size=30)
    y = rng.normal(size=30)
    assert np.isclose(covariance(x, y, ddof=1), np.cov(x, y, ddof=1)[0, 1])


def test_covariance_is_positive_for_positively_related_variables():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([2.0, 4.0, 5.0, 8.0, 10.0])
    assert covariance(x, y) > 0.0


def test_covariance_is_negative_for_inversely_related_variables():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([10.0, 8.0, 5.0, 4.0, 2.0])
    assert covariance(x, y) < 0.0


def test_correlation_of_perfectly_linear_relationship_is_one():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = 2.0 * x + 3.0
    assert np.isclose(correlation(x, y), 1.0)


def test_correlation_of_perfectly_inverse_linear_relationship_is_negative_one():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = -3.0 * x + 1.0
    assert np.isclose(correlation(x, y), -1.0)


def test_correlation_stays_within_valid_range():
    rng = np.random.default_rng(1)
    x = rng.normal(size=50)
    y = rng.normal(size=50)
    result = correlation(x, y)
    assert -1.0 <= result <= 1.0


def test_correlation_is_scale_invariant_unlike_covariance():
    # A well-known property: scaling x by a constant doesn't change the
    # correlation, but does scale the covariance. Directly catches a
    # mutant that returns raw covariance from `correlation`.
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([2.0, 3.0, 5.0, 4.0, 6.0])
    x_scaled = x * 1000.0

    cov_original = covariance(x, y)
    cov_scaled = covariance(x_scaled, y)
    assert not np.isclose(cov_original, cov_scaled)

    corr_original = correlation(x, y)
    corr_scaled = correlation(x_scaled, y)
    assert np.isclose(corr_original, corr_scaled)
