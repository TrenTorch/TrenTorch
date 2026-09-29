"""
pytest data/app_data/01-numpy/03-views-vs-copies/05-the-base-attribute/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/03-views-vs-copies/{Path(__file__).resolve().parent.name}")
owns_its_data = _module.owns_its_data
find_ultimate_owner = _module.find_ultimate_owner


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
