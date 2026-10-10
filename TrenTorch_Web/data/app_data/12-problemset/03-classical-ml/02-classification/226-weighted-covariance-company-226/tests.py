"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]], [1.0, 1.0, 1.0]), [[0.6666666666666666, 0.6666666666666666], [0.6666666666666666, 0.6666666666666666]], atol=1e-6)


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[0.0, 0.0], [0.0, 0.0]], [1.0, 1.0]), [[0.0, 0.0], [0.0, 0.0]], atol=1e-6)


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-1.0, -2.0], [-2.0, -3.0]], [1.0, 1.0]), [[0.25, 0.25], [0.25, 0.25]], atol=1e-6)


def test_all_positive_values():
    np.testing.assert_allclose(solve([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]], [1.0, 2.0, 1.0]), [[0.5, 0.5], [0.5, 0.5]], atol=1e-6)


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[5.0, 5.0]], [1.0]), [[0.0, 0.0], [0.0, 0.0]], atol=1e-6)


def test_repeated_values():
    np.testing.assert_allclose(solve([[2.0, 2.0], [2.0, 2.0]], [1.0, 1.0]), [[0.0, 0.0], [0.0, 0.0]], atol=1e-6)


def test_mixed_signs():
    np.testing.assert_allclose(solve([[-1.0, 1.0], [1.0, -1.0]], [1.0, 1.0]), [[1.0, -1.0], [-1.0, 1.0]], atol=1e-6)


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08, 1e-08], [2e-08, 2e-08]], [1.0, 1.0]), [[2.5000000000000003e-17, 2.5000000000000003e-17], [2.5000000000000003e-17, 2.5000000000000003e-17]], atol=1e-6)


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[1000000.0, 1000000.0], [2000000.0, 2000000.0]], [1.0, 1.0]), [[250000000000.0, 250000000000.0], [250000000000.0, 250000000000.0]], atol=1e-6)


def test_parameter_nudge():
    X = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]
    equal = solve(X, [1.0, 1.0, 1.0])
    skewed = solve(X, [1.0, 1.0, 5.0])
    assert not np.allclose(equal, skewed)


def test_reversed_order():
    X = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]
    w = [1.0, 2.0, 3.0]
    np.testing.assert_allclose(solve(X, w), solve(X[::-1], w[::-1]), atol=1e-9)


def test_large_n_1e5():
    X = np.ones((100000, 2))
    w = np.ones(100000)
    np.testing.assert_allclose(solve(X, w), np.zeros((2, 2)), atol=1e-9)


def test_empty_or_degenerate_input():
    np.testing.assert_allclose(solve(np.zeros((0, 2)), np.zeros(0)), np.zeros((2, 2)))
