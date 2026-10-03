"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
is_view_of = _module.is_view_of
owns_its_data = _module.owns_its_data
find_ultimate_owner = _module.find_ultimate_owner


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


def test_owns_its_data_correct_for_an_owning_array():
    assert owns_its_data(np.array([1, 2, 3])) is True
    assert owns_its_data(np.zeros(5)) is True


def test_owns_its_data_correct_for_a_direct_view():
    arr = np.arange(10)
    assert owns_its_data(arr[2:5]) is False


def test_find_ultimate_owner_on_single_level_view():
    arr = np.arange(10)
    view = arr[2:5]
    assert find_ultimate_owner(view) is arr


def test_find_ultimate_owner_on_multi_level_chain():
    arr = np.arange(10)
    view1 = arr[1:8]
    view2 = view1[2:5]
    view3 = view2[0:2]
    assert find_ultimate_owner(view3) is arr


def test_find_ultimate_owner_when_input_already_owns_its_data():
    arr = np.arange(10)
    assert find_ultimate_owner(arr) is arr
