"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve(np.array([1.0, 2.0]), np.eye(2), np.array([[1.0, 1.0]])), [3.0])


def test_02_zero_input_gives_zero_update():
    np.testing.assert_allclose(solve(np.zeros(2), np.eye(2), np.array([[1.0, 1.0]])), [0.0])


def test_03_negative_input():
    np.testing.assert_allclose(solve(np.array([-1.0, 2.0]), np.eye(2), np.array([[1.0, 1.0]])), [1.0])


def test_04_singleton_boundary():
    np.testing.assert_allclose(solve(np.array([3.0]), np.array([[2.0]]), np.array([[0.5]])), [3.0])
