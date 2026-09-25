"""
pytest data/app_data/01-numpy/03-views-vs-copies/01-what-a-view-is/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/03-views-vs-copies/{Path(__file__).resolve().parent.name}")
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
