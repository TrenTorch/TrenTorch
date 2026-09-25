"""
pytest data/app_data/01-numpy/05-broadcasting/04-incompatible-shapes-and-errors/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/05-broadcasting/{Path(__file__).resolve().parent.name}")
try_broadcast_add = _module.try_broadcast_add
find_first_incompatible_axis = _module.find_first_incompatible_axis


def test_try_broadcast_add_succeeds_for_compatible_shapes():
    a = np.ones((2, 3))
    b = np.array([1, 2, 3])
    result = try_broadcast_add(a, b)
    assert result["success"] is True
    np.testing.assert_array_equal(result["result"], [[2, 3, 4], [2, 3, 4]])


def test_try_broadcast_add_correctly_catches_incompatible_shapes():
    a = np.ones((2, 3))
    b = np.ones((2, 4))
    result = try_broadcast_add(a, b)
    assert result["success"] is False
    assert result["result"] is None


def test_find_first_incompatible_axis_correctly_locates_failure_point():
    assert find_first_incompatible_axis((2, 3), (2, 4)) == -1
    assert find_first_incompatible_axis((2, 3), (5, 3)) == -2


def test_find_first_incompatible_axis_returns_none_for_compatible_shapes():
    assert find_first_incompatible_axis((2, 3), (1, 3)) is None
    assert find_first_incompatible_axis((2, 3), (3,)) is None


def test_equal_total_size_does_not_imply_compatibility():
    a_shape = (6,)
    b_shape = (2, 3)
    assert find_first_incompatible_axis(a_shape, b_shape) == -1
    a = np.ones(a_shape)
    b = np.ones(b_shape)
    assert try_broadcast_add(a, b)["success"] is False
