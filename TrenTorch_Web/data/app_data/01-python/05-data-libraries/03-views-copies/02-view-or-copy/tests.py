"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
classify_operation_result = _module.classify_operation_result


def test_correct_classification_for_all_five_operation_names():
    arr = np.array([1, 2, 3, 4, 5])
    assert classify_operation_result(arr, "basic_slice") == "view"
    assert classify_operation_result(arr, "fancy_index") == "copy"
    assert classify_operation_result(arr, "boolean_mask") == "copy"
    assert classify_operation_result(arr, "arithmetic") == "copy"
    assert classify_operation_result(arr, "explicit_array") == "copy"


def test_works_across_different_array_contents():
    arr = np.array([100, 200, 300, 400, 500, 600])
    assert classify_operation_result(arr, "basic_slice") == "view"
    assert classify_operation_result(arr, "explicit_array") == "copy"


def test_boolean_mask_correctly_classified_even_when_it_selects_most_elements():
    arr = np.array([1, 2, 2, 2, 2])
    mask = arr > arr.mean()
    assert mask.sum() == 4
    result = classify_operation_result(arr, "boolean_mask")
    assert result == "copy"
