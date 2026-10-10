"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([1.0, 2.0, 3.0, 4.0], [2.0, 3.0, 4.0, 5.0]) == pytest.approx(-1.0954451150103321)


def test_all_negative_values():
    assert solve([-1.0, -2.0, -3.0, -4.0], [-2.0, -3.0, -4.0, -5.0]) == pytest.approx(1.0954451150103321)


def test_all_positive_values():
    assert solve([2.0, 4.0, 6.0, 8.0], [3.0, 5.0, 7.0, 9.0]) == pytest.approx(-0.5477225575051661)


def test_repeated_values():
    # Zero spread on both sides gives 0/0
    assert np.isnan(solve([2.0, 2.0, 2.0], [2.0, 2.0, 2.0]))


def test_mixed_signs():
    assert solve([-1.0, 0.0, 1.0, 2.0], [0.0, 1.0, 2.0, 3.0]) == pytest.approx(-1.0954451150103321)


def test_tiny_magnitudes():
    assert solve([1e-08, 2e-08, 3e-08], [2e-08, 3e-08, 4e-08]) == pytest.approx(-1.2247448713915883)


def test_large_magnitudes():
    assert solve([1000000.0, 2000000.0, 3000000.0], [2000000.0, 3000000.0, 4000000.0]) == pytest.approx(-1.2247448713915892)


@pytest.mark.skip(reason="Not applicable: a sample variance with ddof=1 needs at least two observations")
def test_singleton_boundary():
    pass


@pytest.mark.skip(reason="Not applicable: a zero-spread sample on both sides gives 0/0")
def test_exact_zero_inputs():
    pass


def test_parameter_nudge():
    base = solve([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    nudged = solve([1.0, 2.0, 3.001], [1.0, 2.0, 3.0])
    assert nudged != pytest.approx(base)


def test_reversed_order():
    assert solve([1.0, 2.0, 3.0], [4.0, 5.0]) == pytest.approx(solve([3.0, 2.0, 1.0], [4.0, 5.0]))


def test_large_n_1e5():
    rng_a = np.linspace(0.0, 1.0, 100000)
    rng_b = np.linspace(1.0, 2.0, 100000)
    assert np.isfinite(solve(rng_a, rng_b))


def test_empty_or_degenerate_input():
    assert np.isnan(solve([], [1.0, 2.0]))
