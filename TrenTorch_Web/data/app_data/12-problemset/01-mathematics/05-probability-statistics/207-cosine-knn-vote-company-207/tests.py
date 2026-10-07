"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert int(solve([[1.0, 0.0], [0.0, 1.0]], [0, 1], [1.0, 0.0])) == 0


def test_exact_zero_inputs():
    assert int(solve([[1.0, 0.0]], [5], [0.0, 0.0])) == 5


def test_all_negative_values():
    assert int(solve([[-1.0, 0.0], [0.0, -1.0]], [0, 1], [-1.0, 0.0])) == 0


def test_all_positive_values():
    assert int(solve([[1.0, 1.0], [1.0, 0.0]], [0, 1], [1.0, 0.0])) == 1


def test_singleton_boundary():
    assert int(solve([[2.0, 0.0]], [9], [1.0, 0.0])) == 9


def test_repeated_values():
    assert int(solve([[1.0, 0.0], [1.0, 0.0]], [0, 1], [1.0, 0.0])) == 0


def test_mixed_signs():
    assert int(solve([[1.0, 0.0], [-1.0, 0.0]], [0, 1], [1.0, 0.0])) == 0


def test_tiny_magnitudes():
    assert int(solve([[1e-08, 0.0], [0.0, 1e-08]], [0, 1], [1.0, 0.0])) == 0


def test_large_magnitudes():
    assert int(solve([[100000000.0, 0.0], [0.0, 100000000.0]], [0, 1], [1.0, 0.0])) == 0


def test_parameter_nudge():
    X = [[1.0, 0.0], [0.0, 1.0]]
    y = [0, 1]
    assert int(solve(X, y, [1.0, 0.0])) == int(solve(X, y, [2.0, 0.0]))


def test_reversed_order():
    X = [[1.0, 0.0], [0.0, 1.0]]
    assert int(solve(X, [0, 1], [1.0, 0.0])) == int(solve(X[::-1], [1, 0], [1.0, 0.0]))


def test_large_n_1e5():
    X = np.tile([1.0, 0.0], (100000, 1))
    y = np.arange(100000)
    assert int(solve(X, y, [1.0, 0.0])) == 0


def test_empty_or_degenerate_input():
    with pytest.raises(ValueError):
        solve(np.zeros((0, 2)), np.array([]), [1.0, 0.0])
