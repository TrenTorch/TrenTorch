"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
select_by_indices = _module.select_by_indices
select_paired_2d = _module.select_paired_2d
fancy_index_is_copy = _module.fancy_index_is_copy


def test_select_by_indices_correctness_with_reordering_and_repeats():
    arr = np.array([10, 20, 30, 40, 50])
    result = select_by_indices(arr, [3, 0, 0, 1])
    np.testing.assert_array_equal(result, [40, 10, 10, 20])


def test_select_paired_2d_correctness():
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = select_paired_2d(arr, [0, 1, 2], [2, 0, 1])
    np.testing.assert_array_equal(result, [3, 4, 8])


def test_fancy_indexing_always_copies():
    arr = np.array([10, 20, 30, 40, 50])
    result = fancy_index_is_copy(arr, [0, 2, 4])
    assert result["original_unaffected"] is True
    np.testing.assert_array_equal(arr, [10, 20, 30, 40, 50])


def test_out_of_order_and_duplicate_indices_in_2d_pairing():
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = select_paired_2d(arr, [2, 0, 0], [1, 1, 1])
    np.testing.assert_array_equal(result, [8, 2, 2])
