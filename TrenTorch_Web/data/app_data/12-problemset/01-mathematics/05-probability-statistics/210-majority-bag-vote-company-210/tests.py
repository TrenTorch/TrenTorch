"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([0, 1, 1, 2]) == 1


def test_exact_zero_inputs():
    assert solve([0, 0, 0]) == 0


def test_all_positive_values():
    assert solve([1, 1, 2, 2, 2]) == 2


def test_singleton_boundary():
    assert solve([5]) == 5


def test_repeated_values():
    assert solve([3, 3, 3]) == 3


def test_mixed_signs():
    assert solve([0, 1, 0, 2]) == 0


def test_all_negative_values_raises():
    with pytest.raises(ValueError):
        solve([-1, -1, -2])


def test_tie_picks_smallest_label():
    assert solve([0, 1]) == 0


def test_parameter_nudge():
    assert solve([0, 1]) == 0
    assert solve([0, 1, 1]) == 1


def test_reversed_order():
    assert solve([0, 1, 1]) == solve([1, 1, 0])


def test_large_n_1e5():
    predictions = [0] * 60000 + [1] * 40000
    assert solve(predictions) == 0


def test_empty_or_degenerate_input():
    with pytest.raises(ValueError):
        solve([])
