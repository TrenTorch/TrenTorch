"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([1, 0, 1, 1], [1, 1, 1, 0]) == pytest.approx(0.6666666666666666)


def test_exact_zero_inputs():
    assert solve([0, 0, 0], [0, 0, 0]) == pytest.approx(0.0)


def test_all_negative_values():
    assert solve([-1, -1], [-1, -1]) == pytest.approx(1.0)


def test_all_positive_values():
    assert solve([1, 1], [1, 0]) == pytest.approx(1.0)


def test_singleton_boundary():
    assert solve([1], [1]) == pytest.approx(1.0)


def test_repeated_values():
    assert solve([1, 1, 1], [1, 1, 1]) == pytest.approx(1.0)


def test_mixed_signs():
    assert solve([1, 0, -1], [0, 1, 1]) == pytest.approx(0.5)


def test_tiny_magnitudes():
    assert solve([0.0, 1e-08], [1, 1]) == pytest.approx(0.5)


def test_large_magnitudes():
    assert solve([100000000.0, 0.0], [1, 1]) == pytest.approx(0.5)


def test_parameter_nudge():
    base = solve([1, 0], [1, 1])
    with_excluded_pair = solve([1, 0, 1], [1, 1, 0])
    assert with_excluded_pair == pytest.approx(base)


def test_reversed_order():
    assert solve([1, 0], [1, 1]) == pytest.approx(solve([0, 1], [1, 1]))


def test_large_n_1e5():
    ones = np.ones(100000)
    assert solve(ones, ones) == pytest.approx(1.0)


def test_empty_or_degenerate_input():
    assert solve([], []) == 0.0
