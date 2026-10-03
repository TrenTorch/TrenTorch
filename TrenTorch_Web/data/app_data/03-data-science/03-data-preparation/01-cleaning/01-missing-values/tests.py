"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
missing_mask = _module.missing_mask
missing_count_per_column = _module.missing_count_per_column
missing_fraction_per_column = _module.missing_fraction_per_column
impute_with_mean = _module.impute_with_mean
impute_with_median = _module.impute_with_median


nan = np.nan
_X = np.array(
    [
        [1.0, nan, 3.0],
        [nan, nan, 6.0],
        [7.0, 8.0, 9.0],
        [10.0, 11.0, nan],
    ]
)


def test_missing_mask_matches_hand_computation():
    expected = np.array(
        [
            [False, True, False],
            [True, True, False],
            [False, False, False],
            [False, False, True],
        ]
    )
    assert np.array_equal(missing_mask(_X), expected)


def test_missing_mask_of_fully_populated_array_is_all_false():
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert not missing_mask(x).any()


def test_missing_count_per_column_matches_hand_computation():
    # col 0: 1 missing, col 1: 2 missing, col 2: 1 missing
    result = missing_count_per_column(_X)
    assert np.array_equal(result, [1, 2, 1])


def test_missing_fraction_per_column_matches_hand_computation():
    # 4 rows total: col 0 -> 1/4, col 1 -> 2/4, col 2 -> 1/4
    result = missing_fraction_per_column(_X)
    assert np.allclose(result, [0.25, 0.5, 0.25])


def test_missing_fraction_per_column_is_between_zero_and_one():
    result = missing_fraction_per_column(_X)
    assert np.all(result >= 0.0) and np.all(result <= 1.0)


def test_missing_mask_does_not_use_broken_equality_comparison():
    # Directly targets a mutant that checks `x == np.nan` instead of
    # np.isnan(x): that comparison is always False, so a mutant using it
    # would report zero missing values everywhere, even on data that
    # clearly has NaNs.
    result = missing_mask(_X)
    assert result.any()
    assert result.sum() == 4


def test_missing_count_per_column_on_a_fully_missing_column():
    x = np.array([[1.0, nan], [2.0, nan], [3.0, nan]])
    result = missing_count_per_column(x)
    assert np.array_equal(result, [0, 3])


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
