"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_array_equal(solve([[0.0], [10.0], [20.0]], 1), [[True], [False], [True]])


def test_exact_zero_inputs():
    np.testing.assert_array_equal(solve([[0.0], [0.0], [0.0]], 3), [[False], [False], [False]])


def test_all_negative_values():
    np.testing.assert_array_equal(solve([[-20.0], [-10.0], [0.0]], 1), [[True], [False], [True]])


def test_all_positive_values():
    np.testing.assert_array_equal(solve([[5.0], [15.0], [25.0]], 1), [[True], [False], [True]])


def test_singleton_boundary():
    np.testing.assert_array_equal(solve([[5.0]], 3), [[False]])


def test_repeated_values():
    np.testing.assert_array_equal(solve([[3.0], [3.0], [3.0]], 0.5), [[False], [False], [False]])


def test_mixed_signs():
    np.testing.assert_array_equal(solve([[-10.0], [0.0], [10.0]], 1), [[True], [False], [True]])


def test_tiny_magnitudes():
    np.testing.assert_array_equal(solve([[1e-08], [2e-08], [3e-08]], 1), [[True], [False], [True]])


def test_large_magnitudes():
    np.testing.assert_array_equal(solve([[100000000.0], [200000000.0], [300000000.0]], 1), [[True], [False], [True]])


def test_parameter_nudge():
    low = solve([[0.0], [10.0], [20.0]], threshold=1.0)
    high = solve([[0.0], [10.0], [20.0]], threshold=1.3)
    assert int(np.sum(low)) >= int(np.sum(high))


def test_reversed_order():
    x = [[0.0], [10.0], [20.0]]
    np.testing.assert_array_equal(solve(x)[::-1], solve(x[::-1]))


def test_large_n_1e5():
    rng = np.random.default_rng(0)
    x = rng.standard_normal((100000, 1))
    out = solve(x, threshold=3)
    assert out.shape == (100000, 1)
    assert int(out.sum()) < 500


def test_empty_or_degenerate_input():
    out = solve(np.zeros((0, 1)))
    assert out.shape == (0, 1)
