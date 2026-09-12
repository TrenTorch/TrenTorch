"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/04-transpose/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}")
transpose = _module.transpose
is_a_view_of = _module.is_a_view_of


def test_transpose_flips_shape():
    x = np.zeros((3, 5))
    assert transpose(x).shape == (5, 3)


def test_transpose_matches_hand_computation():
    x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    expected = np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]])
    assert np.allclose(transpose(x), expected)


def test_transpose_of_transpose_is_original():
    x = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    assert np.allclose(transpose(transpose(x)), x)


def test_transpose_is_a_view_not_a_copy():
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    t = transpose(x)
    assert is_a_view_of(x, t)


def test_mutating_transposed_view_mutates_the_original():
    # The direct consequence of "transpose is a view": writing through
    # the transposed array changes the original's data too.
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    t = transpose(x)
    t[0, 1] = 99.0
    assert x[1, 0] == 99.0


def test_is_a_view_of_returns_false_for_independent_copies():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([1.0, 2.0, 3.0])  # equal values, separate memory
    assert not is_a_view_of(a, b)


def test_is_a_view_of_is_not_just_checking_equal_values():
    # Directly targets a mutant that implements is_a_view_of as
    # np.array_equal(original, derived) instead of a real memory check:
    # two independently allocated arrays with identical values must
    # report False here, not True.
    a = np.zeros((2, 2))
    b = np.zeros((2, 2))
    assert not is_a_view_of(a, b)
    assert is_a_view_of(a, transpose(a))
