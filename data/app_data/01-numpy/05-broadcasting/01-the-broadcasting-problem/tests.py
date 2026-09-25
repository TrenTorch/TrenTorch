"""
pytest data/app_data/01-numpy/05-broadcasting/01-the-broadcasting-problem/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/05-broadcasting/{Path(__file__).resolve().parent.name}")
add_row_with_loop = _module.add_row_with_loop
add_row_with_broadcasting = _module.add_row_with_broadcasting


def test_both_functions_produce_identical_results():
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    row = np.array([10, 20, 30])
    np.testing.assert_array_equal(
        add_row_with_loop(matrix, row), add_row_with_broadcasting(matrix, row)
    )
    np.testing.assert_array_equal(
        add_row_with_broadcasting(matrix, row), [[11, 22, 33], [14, 25, 36]]
    )


def test_correctness_for_single_row_matrix():
    matrix = np.array([[1, 2, 3]])
    row = np.array([1, 1, 1])
    np.testing.assert_array_equal(add_row_with_loop(matrix, row), [[2, 3, 4]])
    np.testing.assert_array_equal(add_row_with_broadcasting(matrix, row), [[2, 3, 4]])


def test_correctness_for_wider_matrix():
    matrix = np.arange(10).reshape(2, 5)
    row = np.array([1, 2, 3, 4, 5])
    np.testing.assert_array_equal(
        add_row_with_loop(matrix, row), add_row_with_broadcasting(matrix, row)
    )


def test_add_row_with_broadcasting_matches_manual_addition():
    matrix = np.array([[0, 0], [1, 1], [2, 2]])
    row = np.array([5, 10])
    np.testing.assert_array_equal(
        add_row_with_broadcasting(matrix, row), [[5, 10], [6, 11], [7, 12]]
    )
