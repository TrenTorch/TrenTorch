"""
pytest data/app_data/00-math-and-statistics/07-statistical-inference/03-hypothesis-testing-t-test/tests.py
"""

import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/07-statistical-inference/{Path(__file__).resolve().parent.name}"
)
welch_t_statistic = _module.welch_t_statistic
welch_degrees_of_freedom = _module.welch_degrees_of_freedom
two_sample_t_test = _module.two_sample_t_test


def test_t_statistic_is_zero_for_identical_group_means():
    a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    b = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    assert np.isclose(welch_t_statistic(a, b), 0.0)


def test_t_statistic_sign_matches_direction_of_difference():
    a = np.array([10.0, 11.0, 12.0])
    b = np.array([1.0, 2.0, 3.0])
    assert welch_t_statistic(a, b) > 0.0
    assert welch_t_statistic(b, a) < 0.0


def test_t_test_matches_scipy_reference():
    rng = np.random.default_rng(0)
    a = rng.normal(50.0, 10.0, size=30)
    b = rng.normal(55.0, 12.0, size=25)
    t, p = two_sample_t_test(a, b)
    expected = stats.ttest_ind(a, b, equal_var=False)
    assert np.isclose(t, expected.statistic)
    assert np.isclose(p, expected.pvalue)


def test_degrees_of_freedom_matches_scipy_reference():
    rng = np.random.default_rng(1)
    a = rng.normal(0.0, 1.0, size=20)
    b = rng.normal(0.0, 3.0, size=40)
    df = welch_degrees_of_freedom(a, b)
    expected = stats.ttest_ind(a, b, equal_var=False)
    assert np.isclose(df, expected.df)


def test_p_value_is_small_for_a_large_obvious_difference():
    rng = np.random.default_rng(2)
    a = rng.normal(0.0, 1.0, size=100)
    b = rng.normal(20.0, 1.0, size=100)  # dramatically different means
    _, p = two_sample_t_test(a, b)
    assert p < 0.001


def test_p_value_is_large_when_groups_come_from_the_same_distribution():
    rng = np.random.default_rng(3)
    a = rng.normal(0.0, 1.0, size=200)
    b = rng.normal(0.0, 1.0, size=200)
    _, p = two_sample_t_test(a, b)
    assert p > 0.05


def test_p_value_is_symmetric_between_group_orderings():
    rng = np.random.default_rng(4)
    a = rng.normal(10.0, 2.0, size=30)
    b = rng.normal(15.0, 2.0, size=30)
    _, p_ab = two_sample_t_test(a, b)
    _, p_ba = two_sample_t_test(b, a)
    assert np.isclose(p_ab, p_ba)


def test_t_test_does_not_assume_equal_variance():
    # Directly targets a mutant that computes the classic (pooled,
    # equal-variance) Student's t-test instead of Welch's version: with
    # very different sample sizes AND very different variances, the two
    # formulas give visibly different t-statistics.
    rng = np.random.default_rng(5)
    a = rng.normal(0.0, 1.0, size=50)
    b = rng.normal(0.0, 10.0, size=8)  # much smaller, much noisier group
    result = welch_t_statistic(a, b)
    expected_welch = stats.ttest_ind(a, b, equal_var=False).statistic
    expected_pooled = stats.ttest_ind(a, b, equal_var=True).statistic
    assert np.isclose(result, expected_welch)
    assert not np.isclose(result, expected_pooled)
