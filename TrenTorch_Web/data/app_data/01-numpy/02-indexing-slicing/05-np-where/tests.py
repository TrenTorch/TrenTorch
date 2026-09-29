"""
pytest data/app_data/01-numpy/02-indexing-slicing/05-np-where/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/02-indexing-slicing/{Path(__file__).resolve().parent.name}")
find_indices_above = _module.find_indices_above
replace_above_threshold = _module.replace_above_threshold
sign_labels = _module.sign_labels


def test_find_indices_above_correctness():
    arr = np.array([5, 12, 3, 18, 7])
    np.testing.assert_array_equal(find_indices_above(arr, 10), [1, 3])
    np.testing.assert_array_equal(find_indices_above(arr, 100), [])


def test_replace_above_threshold_correctness_and_non_mutation():
    arr = np.array([5, 12, 3, 18, 7])
    result = replace_above_threshold(arr, 10, -1)
    np.testing.assert_array_equal(result, [5, -1, 3, -1, 7])
    np.testing.assert_array_equal(arr, [5, 12, 3, 18, 7])


def test_sign_labels_correctness_including_zero():
    arr = np.array([-2, 0, 3])
    result = sign_labels(arr)
    assert list(result) == ["non-positive", "non-positive", "positive"]


def test_2d_input_handling_for_replace_above_threshold():
    arr = np.array([[5, 15], [25, 2]])
    result = replace_above_threshold(arr, 10, 0)
    np.testing.assert_array_equal(result, [[5, 0], [0, 2]])
