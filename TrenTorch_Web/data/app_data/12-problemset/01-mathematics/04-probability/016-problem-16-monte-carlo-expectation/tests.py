"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve(lambda x: x, [1.0, 2.0, 3.0]) == pytest.approx(2.0)


def test_exact_zero_inputs():
    assert solve(lambda x: x, [0.0, 0.0, 0.0]) == pytest.approx(0.0)


def test_all_negative_values():
    assert solve(lambda x: x, [-1.0, -2.0, -3.0]) == pytest.approx(-2.0)


def test_all_positive_values():
    assert solve(lambda x: x, [2.0, 4.0, 6.0]) == pytest.approx(4.0)


def test_singleton_boundary():
    assert solve(lambda x: x, [5.0]) == pytest.approx(5.0)


def test_repeated_values():
    assert solve(lambda x: x, [3.0, 3.0, 3.0]) == pytest.approx(3.0)


def test_mixed_signs():
    assert solve(lambda x: x, [-2.0, 0.0, 2.0]) == pytest.approx(0.0)


def test_tiny_magnitudes():
    assert solve(lambda x: x, [1e-08, 2e-08]) == pytest.approx(1.5000000000000002e-08)


def test_large_magnitudes():
    assert solve(lambda x: x, [1000000.0, 2000000.0]) == pytest.approx(1500000.0)


def test_parameter_nudge():
    base = solve(lambda x: x, [1.0, 2.0, 3.0])
    nudged = solve(lambda x: x, [1.0, 2.0, 3.003])
    assert nudged - base == pytest.approx(0.001)


def test_reversed_order():
    assert solve(lambda x: x, [1.0, 2.0, 3.0]) == pytest.approx(solve(lambda x: x, [3.0, 2.0, 1.0]))


def test_large_n_1e5():
    samples = np.arange(100000, dtype=float)
    assert solve(lambda x: x, samples) == pytest.approx(49999.5)


def test_empty_or_degenerate_input():
    assert np.isnan(solve(lambda x: x, []))
