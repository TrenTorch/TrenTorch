"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([0.5, 0.5]) == pytest.approx(1.0)


def test_exact_zero_inputs():
    assert solve([0.0, 0.0]) == pytest.approx(0.0)


def test_all_negative_values():
    assert solve([-1.0, -2.0]) == pytest.approx(0.0)


def test_all_positive_values():
    assert solve([0.25, 0.25, 0.25, 0.25]) == pytest.approx(2.0)


def test_singleton_boundary():
    assert solve([1.0]) == pytest.approx(-0.0)


def test_repeated_values():
    assert solve([0.2, 0.2, 0.2, 0.2, 0.2]) == pytest.approx(2.321928094887362)


def test_mixed_signs():
    # Negative and zero entries are ignored, same as if they were absent
    assert solve([-1.0, 0.5, 0.5]) == pytest.approx(solve([0.5, 0.5]))


def test_tiny_magnitudes():
    h = solve([1e-8, 1 - 1e-8])
    assert 0.0 < h < 1e-5


@pytest.mark.skip(reason="Not applicable: probabilities are bounded in [0, 1], there is no large-magnitude case")
def test_large_magnitudes():
    pass


def test_parameter_nudge():
    assert solve([0.5 + 1e-6, 0.5 - 1e-6]) == pytest.approx(1.0, abs=1e-5)


def test_reversed_order():
    assert solve([0.2, 0.3, 0.5]) == pytest.approx(solve([0.5, 0.3, 0.2]))


def test_large_n_1e5():
    p = np.full(100000, 1.0 / 100000)
    assert solve(p) == pytest.approx(np.log2(100000.0), rel=1e-6)


def test_empty_or_degenerate_input():
    assert solve([]) == 0.0
