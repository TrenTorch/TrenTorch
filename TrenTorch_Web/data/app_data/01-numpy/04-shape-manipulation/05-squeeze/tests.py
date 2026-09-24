"""
pytest data/app_data/01-numpy/04-shape-manipulation/05-squeeze/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/04-shape-manipulation/{Path(__file__).resolve().parent.name}")
remove_all_singleton_dims = _module.remove_all_singleton_dims
remove_singleton_at = _module.remove_singleton_at


def test_remove_all_singleton_dims_correctness():
    arr = np.zeros((1, 3, 1, 4))
    assert remove_all_singleton_dims(arr).shape == (3, 4)


def test_remove_singleton_at_correctness_for_specific_axis():
    arr = np.zeros((1, 3, 1, 4))
    assert remove_singleton_at(arr, 0).shape == (3, 1, 4)


def test_no_op_case():
    arr = np.zeros((3, 4))
    assert remove_all_singleton_dims(arr).shape == (3, 4)


def test_values_preserved_exactly():
    arr = np.arange(12).reshape(1, 3, 4)
    result = remove_all_singleton_dims(arr)
    np.testing.assert_array_equal(result, arr.reshape(3, 4))
