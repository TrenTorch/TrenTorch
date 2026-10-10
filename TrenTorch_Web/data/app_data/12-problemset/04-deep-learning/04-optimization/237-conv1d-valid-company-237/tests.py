"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve([1.0, 2.0, 3.0, 4.0], [1.0, 0.0]), [1.0, 2.0, 3.0])


def test_02_difference_kernel():
    np.testing.assert_allclose(solve([1.0, 4.0, 9.0], [1.0, -1.0]), [-3.0, -5.0])


def test_03_singleton_boundary():
    np.testing.assert_allclose(solve([5.0], [2.0]), [10.0])


def test_04_negative_values():
    np.testing.assert_allclose(solve([-1.0, -2.0], [1.0, 1.0]), [-3.0])


def test_05_kernel_longer_than_input_is_empty():
    assert solve([1.0], [1.0, 1.0]).shape == (0,)
