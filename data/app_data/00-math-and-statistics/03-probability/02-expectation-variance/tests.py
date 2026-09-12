"""
pytest data/app_data/00-math-and-statistics/03-probability/02-expectation-variance/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
sample_mean = _module.sample_mean
sample_variance = _module.sample_variance


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
