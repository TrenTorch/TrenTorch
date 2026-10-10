"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    out = solve([1.0, 2.0, 3.0, 0.5], 2, np.random.default_rng(0))
    assert int(out) == 2
    assert int(out) in {1, 2}


def test_exact_zero_inputs():
    out = solve([0.0, 0.0, 0.0], 2, np.random.default_rng(1))
    assert int(out) == 2
    assert int(out) in {1, 2}


def test_all_negative_values():
    out = solve([-1.0, -2.0, -3.0, -4.0], 2, np.random.default_rng(2))
    assert int(out) == 0
    assert int(out) in {0, 1}


def test_all_positive_values():
    out = solve([1.0, 2.0, 3.0, 4.0], 3, np.random.default_rng(3))
    assert int(out) == 1
    assert int(out) in {1, 2, 3}


def test_repeated_values():
    out = solve([2.0, 2.0, 2.0, 2.0], 2, np.random.default_rng(4))
    assert int(out) == 3
    assert int(out) in {2, 3}


def test_mixed_signs():
    out = solve([-3.0, 0.0, 3.0, 1.0], 2, np.random.default_rng(5))
    assert int(out) == 2
    assert int(out) in {2, 3}


def test_large_magnitudes():
    out = solve([1000.0, 1001.0, 999.0], 2, np.random.default_rng(6))
    assert int(out) == 1
    assert int(out) in {0, 1}


def test_singleton_boundary():
    assert int(solve([5.0], 1, np.random.default_rng(0))) == 0


def test_k_equals_length_samples_from_all():
    out = solve([1.0, 2.0, 3.0], 3, np.random.default_rng(7))
    assert int(out) in {0, 1, 2}


def test_large_n_1e5():
    logits = np.zeros(100000)
    logits[42] = 100.0
    out = solve(logits, 1, np.random.default_rng(0))
    assert int(out) == 42
