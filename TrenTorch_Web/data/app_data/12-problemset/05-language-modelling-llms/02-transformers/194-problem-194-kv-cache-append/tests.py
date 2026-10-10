"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve([[1.0, 2.0], [3.0, 4.0]], np.array([5.0, 6.0])), [[1, 2], [3, 4], [5, 6]])


def test_02_empty_cache_gets_one_row():
    out = solve(np.zeros((0, 2)), np.array([1.0, 2.0]))
    np.testing.assert_allclose(out, [[1.0, 2.0]])


def test_03_negative_values_are_kept():
    np.testing.assert_allclose(solve([[-1.0]], np.array([-2.0])), [[-1.0], [-2.0]])


def test_04_appends_at_end():
    out = solve(np.ones((2, 3)), np.zeros(3))
    np.testing.assert_allclose(out[-1], [0.0, 0.0, 0.0])
    assert out.shape == (3, 3)
