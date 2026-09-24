"""
pytest data/app_data/01-numpy/03-views-vs-copies/04-mutating-through-a-view/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/03-views-vs-copies/{Path(__file__).resolve().parent.name}")
zero_out_via_view = _module.zero_out_via_view
chained_view_mutation = _module.chained_view_mutation


def test_zero_out_via_view_mutates_correct_range():
    arr = np.arange(10)
    zero_out_via_view(arr, 2, 5)
    np.testing.assert_array_equal(arr, [0, 1, 0, 0, 0, 5, 6, 7, 8, 9])


def test_zero_out_via_view_does_not_reassign_arr():
    arr = np.arange(10)
    original_id = id(arr)
    zero_out_via_view(arr, 2, 5)
    assert id(arr) == original_id


def test_chained_view_mutation_propagates_through_whole_chain():
    arr = np.arange(10)
    result = chained_view_mutation(arr)
    np.testing.assert_array_equal(arr[3:6], [-1, -1, -1])
    np.testing.assert_array_equal(result["view1"][2:5], [-1, -1, -1])
    np.testing.assert_array_equal(result["view2"], [-1, -1, -1])


def test_elements_outside_innermost_view_range_remain_untouched():
    arr = np.arange(10)
    chained_view_mutation(arr)
    np.testing.assert_array_equal(arr[0:3], [0, 1, 2])
    np.testing.assert_array_equal(arr[6:], [6, 7, 8, 9])
