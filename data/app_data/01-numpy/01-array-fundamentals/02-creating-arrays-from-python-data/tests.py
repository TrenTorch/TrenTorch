"""
pytest data/app_data/01-numpy/01-array-fundamentals/02-creating-arrays-from-python-data/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/01-array-fundamentals/{Path(__file__).resolve().parent.name}")
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
