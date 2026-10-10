"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_equal_components_split_evenly():
    np.testing.assert_allclose(solve(0.0, [0.0, 0.0], [1.0, 1.0], [0.5, 0.5]), [0.5, 0.5], atol=1e-9)


def test_02_closer_mean_gets_more_responsibility():
    e = np.exp(-2.0)
    np.testing.assert_allclose(solve(0.0, [0.0, 2.0], [1.0, 1.0], [0.5, 0.5]), [1 / (1 + e), e / (1 + e)], atol=1e-9)


def test_03_singleton_boundary():
    np.testing.assert_allclose(solve(1.0, [1.0], [2.0], [1.0]), [1.0])


def test_04_responsibilities_sum_to_one():
    assert abs(np.sum(solve(0.3, [0.0, 1.0, 2.0], [1.0, 2.0, 0.5], [0.2, 0.3, 0.5])) - 1.0) < 1e-12
