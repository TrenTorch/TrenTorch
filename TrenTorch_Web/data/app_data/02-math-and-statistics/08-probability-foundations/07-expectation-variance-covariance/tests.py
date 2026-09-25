"""
pytest data/app_data/02-math-and-statistics/08-probability-foundations/07-expectation-variance-covariance/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/08-probability-foundations/07-expectation-variance-covariance")
expectation = _module.expectation
variance = _module.variance
covariance = _module.covariance


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
    result = covariance([0, 1], [0, 1], joint)
    assert np.isclose(result, 0.0, atol=1e-9)


def test_5_covariance_of_perfectly_correlated_variables_equals_the_variance():
    # X and Y always equal (0,0) or (1,1) with equal probability.
    joint = np.array([[0.5, 0.0], [0.0, 0.5]])
    x_values = [0, 1]
    y_values = [0, 1]
    cov = covariance(x_values, y_values, joint)
    var_x = variance(x_values, joint.sum(axis=1))
    assert np.isclose(cov, var_x)


# ---- edge cases ----


def test_6_expectation_of_a_single_outcome():
    result = expectation([42], [1.0])
    assert np.isclose(result, 42.0)


def test_7_covariance_of_negatively_correlated_variables_is_negative():
    # X and Y always take opposite values: (0,1) or (1,0).
    joint = np.array([[0.0, 0.5], [0.5, 0.0]])
    result = covariance([0, 1], [0, 1], joint)
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
    result = covariance([0, 1], [10, 20], joint)
    assert np.isclose(result, 0.0, atol=1e-9)


# ---- independent oracle ----


def test_10_matches_a_hand_computed_reference_case():
    values = [2, 4, 6]
    probabilities = [0.2, 0.5, 0.3]
    mean = expectation(values, probabilities)
    assert np.isclose(mean, 4.2)
    expected_variance = sum(p * (v - mean) ** 2 for v, p in zip(values, probabilities))
    assert np.isclose(variance(values, probabilities), expected_variance)
