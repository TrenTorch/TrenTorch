"""
pytest data/app_data/00-math-and-statistics/05-data-preprocessing/01-detecting-missing-values/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/05-data-preprocessing/{Path(__file__).resolve().parent.name}"
)
missing_mask = _module.missing_mask
missing_count_per_column = _module.missing_count_per_column
missing_fraction_per_column = _module.missing_fraction_per_column

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
