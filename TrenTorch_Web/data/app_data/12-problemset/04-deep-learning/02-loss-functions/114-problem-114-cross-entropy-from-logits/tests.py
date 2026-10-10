"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([1.0, 2.0, 3.0], 2) == pytest.approx(0.4076059644443806)


def test_exact_zero_inputs():
    assert solve([0.0, 0.0, 0.0], 0) == pytest.approx(1.0986122886681098)


def test_all_negative_values():
    assert solve([-1.0, -2.0, -3.0], 0) == pytest.approx(0.40760596444438035)


def test_all_positive_values():
    assert solve([2.0, 4.0, 6.0], 1) == pytest.approx(2.142931628499899)


def test_singleton_boundary():
    assert solve([5.0], 0) == pytest.approx(0.0)


def test_repeated_values():
    assert solve([2.0, 2.0, 2.0], 1) == pytest.approx(1.09861228866811)


def test_mixed_signs():
    assert solve([-3.0, 0.0, 3.0], 2) == pytest.approx(0.05094576352299862)


def test_tiny_magnitudes():
    assert solve([1e-08, 2e-08], 0) == pytest.approx(0.6931471855599453)


def test_large_magnitudes():
    assert solve([1000.0, 2000.0], 1) == pytest.approx(0.0)


def test_parameter_nudge():
    assert solve([1.0, 2.0, 3.0], 2) == pytest.approx(solve([101.0, 102.0, 103.0], 2))


def test_reversed_order():
    assert solve([1.0, 2.0, 3.0], 2) == pytest.approx(solve([3.0, 2.0, 1.0], 0))


def test_large_n_1e5():
    logits = np.zeros(100000)
    assert solve(logits, 0) == pytest.approx(np.log(100000.0))


def test_empty_or_degenerate_input():
    with pytest.raises(ValueError):
        solve([], 0)
