"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[1.0, 2.0], [3.0, 4.0]]), [[10.0, 14.0], [14.0, 20.0]])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[0.0, 0.0], [0.0, 0.0]]), [[0.0, 0.0], [0.0, 0.0]])


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-1.0, -2.0]]), [[1.0, 2.0], [2.0, 4.0]])


def test_all_positive_values():
    np.testing.assert_allclose(solve([[1.0, 2.0]]), [[1.0, 2.0], [2.0, 4.0]])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[2.0]]), [[4.0]])


def test_repeated_values():
    np.testing.assert_allclose(solve([[1.0, 1.0], [1.0, 1.0]]), [[2.0, 2.0], [2.0, 2.0]])


def test_mixed_signs():
    np.testing.assert_allclose(solve([[1.0, -1.0]]), [[1.0, -1.0], [-1.0, 1.0]])


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08]]), [[1.0000000000000001e-16]])


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[10000.0]]), [[100000000.0]])


def test_parameter_nudge():
    X = [[1.0, 2.0], [3.0, 4.0]]
    X2 = [[2.0, 4.0], [6.0, 8.0]]
    np.testing.assert_allclose(solve(X2), 4 * np.array(solve(X)))


def test_reversed_order():
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = solve(X)
    np.testing.assert_allclose(result, result.T)


def test_large_n_1e5():
    X = np.ones((100000, 1))
    np.testing.assert_allclose(solve(X), [[100000.0]])


def test_empty_or_degenerate_input():
    np.testing.assert_allclose(solve(np.zeros((0, 2))), np.zeros((2, 2)))
