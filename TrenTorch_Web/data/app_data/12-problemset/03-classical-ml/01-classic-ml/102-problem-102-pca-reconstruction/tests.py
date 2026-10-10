"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve([[1.0, 2.0]], np.eye(2), 2, np.array([1.0, 1.0])), [[2.0, 3.0]])


def test_02_fewer_components_use_first_column():
    np.testing.assert_allclose(solve([[1.0]], np.eye(2), 1, np.array([1.0, 1.0])), [[2.0, 1.0]])


def test_03_zero_coordinates_return_mean():
    np.testing.assert_allclose(solve([[0.0, 0.0]], np.eye(2), 2, np.array([3.0, -2.0])), [[3.0, -2.0]])


def test_04_singleton_boundary():
    np.testing.assert_allclose(solve([[2.0]], np.array([[0.0], [1.0]]), 1, np.array([0.0, 0.0])), [[0.0, 2.0]])
