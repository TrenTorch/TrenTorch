"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([0.5, 0.5], [[1.0, 2.0], [3.0, 4.0]]), [2.0, 3.0])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([0.0, 0.0], [[1.0, 2.0], [3.0, 4.0]]), [0.0, 0.0])


def test_all_negative_values():
    np.testing.assert_allclose(solve([0.5, 0.5], [[-1.0, -2.0], [-3.0, -4.0]]), [-2.0, -3.0])


def test_all_positive_values():
    np.testing.assert_allclose(solve([0.3, 0.7], [[1.0, 1.0], [2.0, 2.0]]), [1.7, 1.7])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([1.0], [[5.0, 5.0]]), [5.0, 5.0])


def test_repeated_values():
    np.testing.assert_allclose(solve([0.25, 0.25, 0.25, 0.25], [[2.0], [2.0], [2.0], [2.0]]), [2.0])


def test_mixed_signs():
    np.testing.assert_allclose(solve([1.0, -1.0], [[2.0, 2.0], [1.0, 1.0]]), [1.0, 1.0])


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([1e-08, 0.99999999], [[1.0, 0.0], [0.0, 1.0]]), [1e-08, 0.99999999])


def test_large_magnitudes():
    np.testing.assert_allclose(solve([0.5, 0.5], [[1000000.0, 0.0], [0.0, 1000000.0]]), [500000.0, 500000.0])


def test_parameter_nudge():
    np.testing.assert_allclose(solve([1.0, 0.0], [[2.0, 3.0], [4.0, 5.0]]), [2.0, 3.0])


def test_reversed_order():
    weights = [0.2, 0.8]
    values = [[1.0, 0.0], [0.0, 1.0]]
    np.testing.assert_allclose(solve(weights, values), solve(weights[::-1], values[::-1]))


def test_large_n_1e5():
    weights = np.full(100000, 1.0 / 100000)
    values = np.ones((100000, 2))
    np.testing.assert_allclose(solve(weights, values), [1.0, 1.0])


def test_empty_or_degenerate_input():
    out = solve(np.zeros(0), np.zeros((0, 2)))
    np.testing.assert_allclose(out, [0.0, 0.0])
