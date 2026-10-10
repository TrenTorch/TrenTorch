"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([3, 1]) == pytest.approx(0.8112781244591328)


def test_exact_zero_inputs():
    assert solve([0, 0]) == pytest.approx(0.0)


def test_all_positive_values():
    assert solve([2, 2, 2, 2]) == pytest.approx(2.0)


def test_singleton_boundary():
    assert solve([5]) == pytest.approx(-0.0)


def test_repeated_values():
    assert solve([4, 4]) == pytest.approx(1.0)


def test_large_magnitudes():
    assert solve([1000000, 1000000]) == pytest.approx(1.0)


@pytest.mark.skip(reason="Not applicable: class counts are non-negative by definition")
def test_all_negative_values():
    pass


@pytest.mark.skip(reason="Not applicable: counts have no sign to mix")
def test_mixed_signs():
    pass


def test_tiny_magnitudes():
    assert solve([1, 0]) == pytest.approx(0.0)


def test_parameter_nudge():
    assert solve([1, 1]) == pytest.approx(1.0)
    assert solve([1, 1, 1, 1]) == pytest.approx(2.0)


def test_reversed_order():
    assert solve([3, 1]) == pytest.approx(solve([1, 3]))


def test_large_n_1e5():
    assert solve([1] * 100000) == pytest.approx(np.log2(100000.0), rel=1e-6)


def test_empty_or_degenerate_input():
    assert solve([]) == 0.0
