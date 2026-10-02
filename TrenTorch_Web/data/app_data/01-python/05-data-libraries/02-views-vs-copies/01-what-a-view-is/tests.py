"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
is_view_of = _module.is_view_of


def test_slice_correctly_identified_as_sharing_memory():
    arr = np.arange(10)
    view = arr[2:5]
    assert is_view_of(view, arr) is True


def test_independently_created_array_correctly_identified_as_not_sharing_memory():
    a = np.array([1, 2, 3])
    b = np.array([1, 2, 3])
    assert is_view_of(a, b) is False


def test_np_array_copy_correctly_identified_as_not_sharing_memory():
    arr = np.arange(5)
    copy = np.array(arr)
    assert is_view_of(copy, arr) is False


def test_order_independence():
    arr = np.arange(10)
    view = arr[2:5]
    assert is_view_of(view, arr) == is_view_of(arr, view)
