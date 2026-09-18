"""
pytest data/app_data/02-deep-learning-core/01-tensors/07-indexing-slicing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/01-tensors/{Path(__file__).resolve().parent.name}")
basic_slice = _module.basic_slice
boolean_mask = _module.boolean_mask
fancy_index = _module.fancy_index
is_a_view_of = _module.is_a_view_of


def test_basic_slice_values():
    a = np.arange(10)
    assert np.array_equal(basic_slice(a, 2, 5), [2, 3, 4])


def test_boolean_mask_values():
    a = np.arange(10)
    result = boolean_mask(a, a % 2 == 0)
    assert np.array_equal(result, [0, 2, 4, 6, 8])


def test_fancy_index_values():
    a = np.arange(10)
    result = fancy_index(a, np.array([1, 3, 5]))
    assert np.array_equal(result, [1, 3, 5])


def test_basic_slice_is_a_view():
    a = np.arange(10)
    result = basic_slice(a, 2, 5)
    assert is_a_view_of(result, a) is True


def test_boolean_mask_is_a_copy_not_a_view():
    a = np.arange(10)
    result = boolean_mask(a, a % 2 == 0)
    assert is_a_view_of(result, a) is False


def test_fancy_index_is_a_copy_not_a_view():
    a = np.arange(10)
    result = fancy_index(a, np.array([1, 3, 5]))
    assert is_a_view_of(result, a) is False


def test_mutating_a_slice_view_changes_the_original():
    a = np.arange(10)
    sliced = basic_slice(a, 2, 5)
    sliced[0] = 999
    assert a[2] == 999  # shared memory, the mutation shows through


def test_mutating_a_fancy_indexed_copy_leaves_the_original_untouched():
    a = np.arange(10)
    indexed = fancy_index(a, np.array([1, 3, 5]))
    indexed[0] = 999
    assert a[1] == 1  # independent copy, the mutation does NOT show through
