"""
pytest data/app_data/01-numpy/04-shape-manipulation/06-combining-arrays/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/04-shape-manipulation/{Path(__file__).resolve().parent.name}")
join_along_existing_axis = _module.join_along_existing_axis
stack_as_new_axis = _module.stack_as_new_axis
side_by_side = _module.side_by_side
stacked_vertically = _module.stacked_vertically


def test_join_along_existing_axis_correctness_for_axis_0_and_1():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6]])
    result0 = join_along_existing_axis([a, b], 0)
    np.testing.assert_array_equal(result0, [[1, 2], [3, 4], [5, 6]])

    c = np.array([[1], [2]])
    result1 = join_along_existing_axis([a, c], 1)
    np.testing.assert_array_equal(result1, [[1, 2, 1], [3, 4, 2]])


def test_stack_as_new_axis_introduces_genuinely_new_dimension():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    result = stack_as_new_axis([a, b])
    assert result.shape == (2, 3)
    assert result.ndim == a.ndim + 1


def test_concatenate_vs_stack_produce_different_dimensionality_on_same_1d_inputs():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    concatenated = join_along_existing_axis([a, b], 0)
    stacked = stack_as_new_axis([a, b])
    assert concatenated.ndim == 1
    assert stacked.ndim == 2


def test_side_by_side_and_stacked_vertically_correctness():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    np.testing.assert_array_equal(side_by_side(a, b), [[1, 2, 5, 6], [3, 4, 7, 8]])
    np.testing.assert_array_equal(
        stacked_vertically(a, b), [[1, 2], [3, 4], [5, 6], [7, 8]]
    )


def test_all_four_functions_produce_independent_copies():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])

    result = side_by_side(a, b)
    result[0, 0] = -1
    np.testing.assert_array_equal(a, [[1, 2], [3, 4]])

    result = stacked_vertically(a, b)
    result[0, 0] = -1
    np.testing.assert_array_equal(a, [[1, 2], [3, 4]])

    result = stack_as_new_axis([a, b])
    result[0, 0, 0] = -1
    np.testing.assert_array_equal(a, [[1, 2], [3, 4]])
