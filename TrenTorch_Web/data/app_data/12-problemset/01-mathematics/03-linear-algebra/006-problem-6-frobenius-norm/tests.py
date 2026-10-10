"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([[3.0, 4.0]]) == pytest.approx(5.0)


def test_exact_zero_inputs():
    assert solve([[0.0, 0.0], [0.0, 0.0]]) == pytest.approx(0.0)


def test_all_negative_values():
    assert solve([[-3.0, -4.0]]) == pytest.approx(5.0)


def test_all_positive_values():
    assert solve([[1.0, 2.0], [2.0, 1.0]]) == pytest.approx(3.1622776601683795)


def test_singleton_boundary():
    assert solve([[5.0]]) == pytest.approx(5.0)


def test_repeated_values():
    assert solve([[2.0, 2.0], [2.0, 2.0]]) == pytest.approx(4.0)


def test_mixed_signs():
    assert solve([[-3.0, 4.0]]) == pytest.approx(5.0)


def test_tiny_magnitudes():
    assert solve([[1e-08, 0.0]]) == pytest.approx(1e-08)


def test_large_magnitudes():
    assert solve([[10000.0, 0.0]]) == pytest.approx(10000.0)


def test_parameter_nudge():
    A = [[2.0, 0.0], [0.0, 2.0]]
    assert solve([[c * 2 for c in row] for row in A]) == pytest.approx(2 * solve(A))


def test_reversed_order():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[4.0, 3.0], [2.0, 1.0]]
    assert solve(A) == pytest.approx(solve(B))


def test_large_n_1e5():
    A = np.ones((1, 100000))
    assert solve(A) == pytest.approx(np.sqrt(100000.0))


def test_empty_or_degenerate_input():
    assert solve(np.zeros((0, 0))) == 0.0
