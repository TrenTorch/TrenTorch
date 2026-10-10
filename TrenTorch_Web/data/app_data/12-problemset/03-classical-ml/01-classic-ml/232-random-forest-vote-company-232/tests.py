"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    assert solve([[0.2, 0.8], [0.6, 0.4]]) == 1


def test_exact_zero_inputs():
    assert solve([[0.0, 0.0], [0.0, 0.0]]) == 0


def test_all_positive_values():
    assert solve([[0.1, 0.9], [0.2, 0.8]]) == 1


def test_singleton_boundary():
    assert solve([[0.3, 0.7]]) == 1


def test_repeated_values():
    assert solve([[0.5, 0.5], [0.5, 0.5]]) == 0


def test_tie_picks_first_class():
    assert solve([[0.5, 0.5]]) == 0


def test_reversed_order():
    P = [[0.2, 0.8], [0.6, 0.4]]
    assert solve(P) == solve(P[::-1])


def test_large_n_1e5():
    P = np.tile([0.1, 0.9], (100000, 1))
    assert solve(P) == 1
