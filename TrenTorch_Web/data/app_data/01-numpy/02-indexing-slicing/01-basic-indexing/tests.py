"""
pytest data/app_data/01-numpy/02-indexing-slicing/01-basic-indexing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/02-indexing-slicing/{Path(__file__).resolve().parent.name}")
get_element_1d = _module.get_element_1d
get_element_2d = _module.get_element_2d
get_row = _module.get_row


def test_positive_and_negative_index_correctness_1d():
    arr = np.array([10, 20, 30, 40])
    assert get_element_1d(arr, 0) == 10
    assert get_element_1d(arr, -1) == 40
    assert get_element_1d(arr, 2) == 30


def test_2d_indexing_correctness_across_rows_and_columns():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    assert get_element_2d(arr, 0, 0) == 1
    assert get_element_2d(arr, 1, 2) == 6
    assert get_element_2d(arr, 0, 2) == 3


def test_negative_indices_in_2d():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    assert get_element_2d(arr, -1, -1) == 6
    assert get_element_2d(arr, -1, 0) == 4


def test_get_row_returns_full_valid_subarray():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    row = get_row(arr, 1)
    assert row.shape == (3,)
    np.testing.assert_array_equal(row, [4, 5, 6])
