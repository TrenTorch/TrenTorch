"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) == pytest.approx(-3.0)


def test_exact_zero_inputs():
    assert solve([0.0, 0.0], [0.0, 0.0]) == pytest.approx(0.0)


def test_all_negative_values():
    assert solve([-1.0, -2.0], [-3.0, -4.0]) == pytest.approx(2.0)


def test_all_positive_values():
    assert solve([2.0, 4.0], [1.0, 1.0]) == pytest.approx(2.0)


def test_singleton_boundary():
    assert solve([5.0], [2.0]) == pytest.approx(3.0)


def test_repeated_values():
    assert solve([2.0, 2.0, 2.0], [2.0, 2.0, 2.0]) == pytest.approx(0.0)


def test_mixed_signs():
    assert solve([-1.0, 1.0], [0.0, 0.0]) == pytest.approx(0.0)


def test_tiny_magnitudes():
    assert solve([1e-08], [2e-08]) == pytest.approx(-1e-08)


def test_large_magnitudes():
    assert solve([100000000.0], [200000000.0]) == pytest.approx(-100000000.0)


def test_parameter_nudge():
    base = solve([1.0, 2.0, 3.0], [1.0, 1.0, 1.0])
    nudged = solve([1.0, 2.0, 3.003], [1.0, 1.0, 1.0])
    assert nudged - base == pytest.approx(0.001)


def test_reversed_order():
    assert solve([1.0, 2.0, 3.0], [1.0]) == pytest.approx(solve([3.0, 2.0, 1.0], [1.0]))


def test_large_n_1e5():
    a = np.full(100000, 5.0)
    b = np.full(100000, 3.0)
    assert solve(a, b) == pytest.approx(2.0)


def test_empty_or_degenerate_input():
    assert np.isnan(solve([], [1.0, 2.0]))
