"""
pytest data/app_data/00-math-and-statistics/06-exploratory-data-analysis/02-summarizing-distribution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/06-exploratory-data-analysis/{Path(__file__).resolve().parent.name}"
)
skewness = _module.skewness
summarize_distribution = _module.summarize_distribution


def test_skewness_of_symmetric_data_is_near_zero():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    assert np.isclose(skewness(x), 0.0, atol=1e-9)


def test_skewness_of_right_skewed_data_is_positive():
    x = np.array([1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 20.0])
    assert skewness(x) > 0.0


def test_skewness_of_left_skewed_data_is_negative():
    x = np.array([-20.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0])
    assert skewness(x) < 0.0


def test_skewness_matches_known_oracle_value():
    # generated once, offline, via scipy.stats.skew
    x = np.array([1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 20.0])
    expected = 2.6524012569745175
    assert np.isclose(skewness(x), expected, atol=1e-9)


def test_summarize_distribution_returns_expected_keys():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = summarize_distribution(x)
    assert set(result.keys()) == {"mean", "median", "std", "skew"}


def test_summarize_distribution_values_match_individual_computations():
    x = np.array([1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 20.0])
    result = summarize_distribution(x)
    assert np.isclose(result["mean"], np.mean(x))
    assert np.isclose(result["median"], np.median(x))
    assert np.isclose(result["std"], np.std(x))
    assert np.isclose(result["skew"], skewness(x))


def test_summarize_distribution_flags_a_large_mean_median_gap_for_skewed_data():
    x = np.array([1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 100.0])
    result = summarize_distribution(x)
    assert result["mean"] > result["median"] + 3.0  # mean dragged up by the tail
    assert result["skew"] > 0.0


def test_skewness_uses_cube_not_square():
    # Directly targets a mutant that squares instead of cubes (i.e.
    # copies variance's formula): squaring always gives a non-negative
    # result, losing skewness's defining "which direction does it lean"
    # sign information entirely.
    x = np.array([-20.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0])
    result = skewness(x)
    assert result < 0.0  # a squared version could never be negative
