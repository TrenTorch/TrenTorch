"""
pytest data/app_data/01-numpy/02-indexing-slicing/03-boolean-masking/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/02-indexing-slicing/{Path(__file__).resolve().parent.name}")
select_above_threshold = _module.select_above_threshold
select_in_range = _module.select_in_range
zero_out_negatives = _module.zero_out_negatives


def test_select_above_threshold_correctness():
    arr = np.array([10, 15, 20, 25, 30])
    result = select_above_threshold(arr, 18)
    np.testing.assert_array_equal(result, [20, 25, 30])
    assert 18 not in select_above_threshold(np.array([18]), 18)


def test_select_in_range_correctness_with_combined_condition():
    arr = np.array([5, 10, 15, 20, 25])
    result = select_in_range(arr, 10, 20)
    np.testing.assert_array_equal(result, [15])


def test_masking_returns_copy_not_view():
    arr = np.array([10, 15, 20, 25, 30])
    result = select_above_threshold(arr, 18)
    result[0] = -1
    np.testing.assert_array_equal(arr, [10, 15, 20, 25, 30])


def test_zero_out_negatives_mutates_in_place():
    arr = np.array([-1, 2, -3, 4])
    original_id = id(arr)
    zero_out_negatives(arr)
    assert id(arr) == original_id
    np.testing.assert_array_equal(arr, [0, 2, 0, 4])


def test_all_true_and_all_false_mask_edge_cases():
    all_above = select_above_threshold(np.array([5, 6, 7]), 0)
    np.testing.assert_array_equal(all_above, [5, 6, 7])
    none_above = select_above_threshold(np.array([5, 6, 7]), 100)
    assert none_above.size == 0
