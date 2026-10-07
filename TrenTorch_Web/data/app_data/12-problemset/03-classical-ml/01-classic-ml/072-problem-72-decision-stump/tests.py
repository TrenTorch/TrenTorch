"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    out = solve([1.0, 2.0, 3.0, 4.0], [0, 0, 1, 1])
    assert out == (2.0, 0, 1)


def test_all_negative_values():
    out = solve([-4.0, -3.0, -2.0, -1.0], [1, 1, 0, 0])
    assert out == (-3.0, 1, 0)


def test_all_positive_values():
    out = solve([1.0, 2.0, 3.0, 4.0], [1, 1, 0, 0])
    assert out == (2.0, 1, 0)


def test_repeated_values():
    out = solve([1.0, 1.0, 2.0, 2.0], [0, 0, 1, 1])
    assert out == (1.0, 0, 1)


def test_mixed_signs():
    out = solve([-2.0, -1.0, 1.0, 2.0], [0, 0, 1, 1])
    assert out == (-1.0, 0, 1)


def test_tiny_magnitudes():
    out = solve([1e-08, 2e-08, 3e-08, 4e-08], [0, 0, 1, 1])
    assert out == (2e-08, 0, 1)


def test_large_magnitudes():
    out = solve([1000000.0, 2000000.0, 3000000.0, 4000000.0], [0, 0, 1, 1])
    assert out == (2000000.0, 0, 1)


def test_singleton_boundary():
    with pytest.raises(ValueError):
        solve([1.0], [0])


def test_exact_zero_inputs():
    with pytest.raises(ValueError):
        solve([0.0, 0.0], [0, 0])


def test_reversed_order():
    assert solve([1.0, 2.0, 3.0, 4.0], [0, 0, 1, 1]) == solve([4.0, 3.0, 2.0, 1.0], [1, 1, 0, 0])


def test_large_n_1e5():
    # The reference split search is O(n^2); use a smaller size that still exercises
    # the same code path within a reasonable time.
    x = np.arange(2000, dtype=float)
    y = (x >= 1000).astype(int)
    threshold, left_mode, right_mode = solve(x, y)
    assert threshold == pytest.approx(999.0)
    assert (left_mode, right_mode) == (0, 1)
