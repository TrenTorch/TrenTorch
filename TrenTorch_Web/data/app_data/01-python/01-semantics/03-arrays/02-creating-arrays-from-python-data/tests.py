"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
list_to_array = _module.list_to_array
nested_list_to_array = _module.nested_list_to_array


def test_1d_conversion_preserves_values_and_order():
    result = list_to_array([3, 1, 4, 1, 5])
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, [3, 1, 4, 1, 5])


def test_2d_conversion_produces_correct_shape():
    result = nested_list_to_array([[1, 2, 3], [4, 5, 6]])
    assert result.shape == (2, 3)


def test_2d_conversion_preserves_row_structure():
    result = nested_list_to_array([[1, 2], [3, 4]])
    np.testing.assert_array_equal(result[0], [1, 2])
    np.testing.assert_array_equal(result[1], [3, 4])


def test_result_does_not_share_memory_with_original_list():
    original = [1, 2, 3]
    result = list_to_array(original)
    original[0] = 999
    assert result[0] == 1
