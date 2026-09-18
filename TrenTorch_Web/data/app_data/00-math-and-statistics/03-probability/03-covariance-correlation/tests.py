"""
pytest data/app_data/00-math-and-statistics/03-probability/03-covariance-correlation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
covariance = _module.covariance
correlation = _module.correlation


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
