"""
pytest data/app_data/00-math-and-statistics/05-data-preprocessing/02-imputing-missing-values/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/05-data-preprocessing/{Path(__file__).resolve().parent.name}"
)
impute_with_mean = _module.impute_with_mean
impute_with_median = _module.impute_with_median

nan = np.nan


def test_impute_with_mean_matches_hand_computation():
    x = np.array([[1.0, nan], [2.0, 4.0], [nan, 6.0]])
    # col 0: mean of [1,2] = 1.5, col 1: mean of [4,6] = 5.0
    result = impute_with_mean(x)
    assert np.allclose(result, [[1.0, 5.0], [2.0, 4.0], [1.5, 6.0]])


def test_impute_with_median_matches_hand_computation():
    x = np.array([[1.0, nan], [2.0, 4.0], [3.0, 6.0], [nan, 100.0]])
    # col 0: median of [1,2,3] = 2.0
    # col 1: median of [4,6,100] = 6.0
    result = impute_with_median(x)
    assert np.allclose(result, [[1.0, 6.0], [2.0, 4.0], [3.0, 6.0], [2.0, 100.0]])


def test_impute_functions_leave_non_missing_values_unchanged():
    x = np.array([[1.0, 2.0], [3.0, nan]])
    result = impute_with_mean(x)
    assert result[0, 0] == 1.0
    assert result[0, 1] == 2.0
    assert result[1, 0] == 3.0


def test_impute_functions_do_not_mutate_the_input():
    x = np.array([[1.0, nan], [3.0, 4.0]])
    x_copy = x.copy()
    impute_with_mean(x)
    assert np.array_equal(x, x_copy, equal_nan=True)


def test_impute_result_has_no_remaining_nans():
    x = np.array([[1.0, nan], [nan, 4.0], [5.0, 6.0]])
    assert not np.isnan(impute_with_mean(x)).any()
    assert not np.isnan(impute_with_median(x)).any()


def test_median_imputation_is_robust_to_outliers_unlike_mean():
    # A single huge outlier drags the mean far from "typical", but
    # barely moves the median.
    x = np.array([[1.0], [2.0], [3.0], [1000.0], [nan]])
    mean_result = impute_with_mean(x)[4, 0]
    median_result = impute_with_median(x)[4, 0]
    assert mean_result > 200.0  # dragged upward by the outlier
    assert median_result < 5.0  # stays close to the "typical" values


def test_impute_uses_own_column_not_a_different_column():
    # Directly targets a mutant that fills every missing value with a
    # single global statistic instead of each value's OWN column's
    # statistic. With very different column means, filling from the
    # wrong column produces a clearly wrong number.
    x = np.array([[1.0, 100.0], [2.0, nan], [3.0, 300.0]])
    result = impute_with_mean(x)
    # col 1 mean (excluding NaN) = (100+300)/2 = 200, NOT col 0's mean (2.0)
    assert np.isclose(result[1, 1], 200.0)
    assert not np.isclose(result[1, 1], 2.0)
