"""
pytest data/app_data/01-numpy/04-shape-manipulation/01-reshape/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/04-shape-manipulation/{Path(__file__).resolve().parent.name}")
reshape_to = _module.reshape_to
reshape_with_inferred_dim = _module.reshape_with_inferred_dim
reshape_shares_memory = _module.reshape_shares_memory


def test_reshape_to_correctness_across_dimensions():
    arr = np.arange(12)
    np.testing.assert_array_equal(reshape_to(arr, (3, 4)), arr.reshape(3, 4))
    np.testing.assert_array_equal(reshape_to(arr, (2, 3, 2)), arr.reshape(2, 3, 2))


def test_reshape_with_inferred_dim_correct_automatic_dimension():
    arr = np.arange(12)
    result = reshape_with_inferred_dim(arr, 4)
    assert result.shape == (3, 4)
    result2 = reshape_with_inferred_dim(arr, 6)
    assert result2.shape == (2, 6)


def test_reshape_raises_on_incompatible_size():
    arr = np.arange(12)
    with pytest.raises(ValueError):
        reshape_to(arr, (3, 5))


def test_reshape_shares_memory_correctly_reports_view_case():
    arr = np.arange(6)
    assert reshape_shares_memory(arr, (2, 3)) is True


def test_values_preserved_in_correct_order_after_reshape():
    arr = np.arange(6)
    result = reshape_to(arr, (2, 3))
    np.testing.assert_array_equal(result[0], [0, 1, 2])
    np.testing.assert_array_equal(result[1], [3, 4, 5])
