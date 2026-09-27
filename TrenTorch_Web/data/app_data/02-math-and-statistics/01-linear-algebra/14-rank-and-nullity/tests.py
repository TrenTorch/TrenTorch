"""
pytest data/app_data/02-math-and-statistics/01-linear-algebra/14-rank-and-nullity/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/01-linear-algebra/14-rank-and-nullity")
rank = _module.rank
nullity = _module.nullity


# ---- 1-2: basic correctness ----


def test_1_full_rank_2x2_matrix():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert rank(A) == 2


def test_2_rank_deficient_matrix():
    A = np.array([[1.0, 2.0], [2.0, 4.0]])  # row 2 = 2 * row 1
    assert rank(A) == 1


# ---- shape / general-case coverage ----


def test_3_identity_matrix_is_full_rank():
    assert rank(np.eye(4)) == 4


def test_4_rectangular_wide_matrix():
    A = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])  # (2, 3), full row rank
    assert rank(A) == 2


def test_5_rectangular_tall_matrix():
    A = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # (3, 2), full column rank
    assert rank(A) == 2


def test_6_nullity_follows_rank_nullity_theorem():
    A = np.array([[1.0, 2.0], [2.0, 4.0]])  # rank 1, 2 columns
    assert nullity(A) == 1


# ---- edge cases ----


def test_7_zero_matrix_has_rank_zero():
    A = np.zeros((3, 3))
    assert rank(A) == 0
    assert nullity(A) == 3


def test_8_single_row_matrix():
    A = np.array([[1.0, 2.0, 3.0]])
    assert rank(A) == 1


def test_9_3x3_rank_deficient_by_two():
    A = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0]])  # all rows parallel
    assert rank(A) == 1
    assert nullity(A) == 2


# ---- mutation-catching ----


def test_10_pivot_zero_column_is_skipped_not_treated_as_a_rank_boost():
    # A wrong implementation that advances the row pointer even when no
    # pivot is found in a column would overcount rank here.
    A = np.array([[0.0, 1.0], [0.0, 2.0]])  # first column all zero, rank should be 1
    assert rank(A) == 1


def test_11_row_swap_needed_to_find_a_pivot():
    # The first row's leading entry is zero, so a correct implementation
    # must look further down the column for a usable pivot.
    A = np.array([[0.0, 1.0], [1.0, 0.0]])
    assert rank(A) == 2


def test_12_input_array_is_not_mutated():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    original = A.copy()
    rank(A)
    np.testing.assert_array_equal(A, original)


# ---- independent oracle ----


def test_13_matches_numpy_matrix_rank_reference():
    matrices = [
        np.array([[1.0, 2.0], [3.0, 4.0]]),
        np.array([[1.0, 2.0], [2.0, 4.0]]),
        np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0], [1.0, 1.0, 5.0]]),
    ]
    for A in matrices:
        assert rank(A) == np.linalg.matrix_rank(A)
