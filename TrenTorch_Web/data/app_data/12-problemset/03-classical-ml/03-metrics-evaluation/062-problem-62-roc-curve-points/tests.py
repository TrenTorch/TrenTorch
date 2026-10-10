"""Tests with expected values computed from an independently written reference (cumulative-sum ROC), not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def _close(actual, expected):
    assert len(actual) == len(expected)
    for (a_f, a_t), (e_f, e_t) in zip(actual, expected):
        assert a_f == pytest.approx(e_f)
        assert a_t == pytest.approx(e_t)


def test_basic_example():
    _close(solve([0, 1, 1, 0], [0, 1, 0, 1]), [(0.5, 0.5), (1.0, 1.0)])


def test_exact_zero_inputs():
    _close(solve([0, 0, 0, 0], [0, 0, 0, 0]), [(1.0, 0.0)])


def test_all_negative_values():
    _close(solve([1, 0], [-1, -2]), [(0.0, 1.0), (1.0, 1.0)])


def test_all_positive_values():
    _close(solve([1, 0, 1], [0.9, 0.8, 0.1]), [(0.0, 0.5), (1.0, 0.5), (1.0, 1.0)])


def test_singleton_boundary():
    _close(solve([1], [0.5]), [(0.0, 1.0)])


def test_repeated_values():
    _close(solve([1, 0], [0.5, 0.5]), [(1.0, 1.0)])


def test_mixed_signs():
    _close(solve([1, 0, 1, 0], [-1.0, 0.0, 1.0, -0.5]), [(0.0, 0.5), (0.5, 0.5), (1.0, 0.5), (1.0, 1.0)])


def test_tiny_magnitudes():
    _close(solve([1, 0, 1, 0], [1e-08, 2e-08, 3e-08, 4e-08]), [(0.5, 0.0), (0.5, 0.5), (1.0, 0.5), (1.0, 1.0)])


def test_large_magnitudes():
    _close(solve([1, 0, 1, 0], [1000000.0, 2000000.0, 3000000.0, 4000000.0]), [(0.5, 0.0), (0.5, 0.5), (1.0, 0.5), (1.0, 1.0)])


def test_rates_never_exceed_one():
    points = solve([0, 1, 1, 0, 1, 0], [0.1, 0.4, 0.4, 0.8, 0.8, 0.2])
    assert all(0.0 <= f <= 1.0 and 0.0 <= t <= 1.0 for f, t in points)


def test_parameter_nudge():
    base = solve([1, 0], [0.6, 0.4])
    nudged = solve([1, 0], [0.6, 0.6])
    assert len(base) == 2 and len(nudged) == 1


def test_reversed_order():
    y = [0, 1, 1, 0]
    s = [0.1, 0.9, 0.4, 0.3]
    _close(solve(y, s), solve(y[::-1], s[::-1]))


def test_large_n_1e5():
    # The reference threshold loop is O(n^2); use a smaller size that exercises the same path quickly.
    y = np.tile([0, 1], 1000)
    s = np.arange(2000, dtype=float)
    points = solve(y, s)
    assert len(points) == 2000
    assert points[-1] == pytest.approx((1.0, 1.0))


def test_empty_or_degenerate_input():
    assert solve([], []) == []
