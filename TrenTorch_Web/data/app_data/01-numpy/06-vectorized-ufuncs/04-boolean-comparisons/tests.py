"""
pytest data/app_data/01-numpy/06-vectorized-ufuncs/04-boolean-comparisons/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/06-vectorized-ufuncs/{Path(__file__).resolve().parent.name}")
in_range_mask = _module.in_range_mask
outside_range_mask = _module.outside_range_mask
not_matching = _module.not_matching


def test_in_range_mask_correctness_including_boundaries():
    arr = np.array([5, 10, 15, 20])
    result = in_range_mask(arr, 10, 20)
    np.testing.assert_array_equal(result, [False, False, True, False])


def test_outside_range_mask_correctness():
    arr = np.array([5, 10, 15, 20])
    result = outside_range_mask(arr, 10, 20)
    np.testing.assert_array_equal(result, [True, False, False, False])


def test_not_matching_correctness():
    arr = np.array([1, 2, 1, 3])
    result = not_matching(arr, 1)
    np.testing.assert_array_equal(result, [False, True, False, True])


def test_python_and_or_on_multi_element_array_raises_error():
    arr = np.array([5, 12, 3, 18])
    try:
        _ = (arr > 10) and (arr < 15)
        raised = False
    except ValueError:
        raised = True
    assert raised is True


def test_correct_operator_precedence_handling():
    arr = np.array([5, 12, 3, 18])
    result = in_range_mask(arr, 10, 15)
    np.testing.assert_array_equal(result, [False, True, False, False])
