"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve([0.0, 0.0], [[1.0, 2.0], [3.0, 4.0]]), [2.0, 3.0])


def test_02_weights_follow_softmax():
    e = np.exp(1.0)
    w = np.array([1 / (1 + e), e / (1 + e)])
    np.testing.assert_allclose(solve([0.0, 1.0], [[1.0, 2.0], [3.0, 4.0]]), w @ np.array([[1.0, 2.0], [3.0, 4.0]]), atol=1e-9)


def test_03_single_value_is_returned():
    np.testing.assert_allclose(solve([5.0], [[7.0, -2.0]]), [7.0, -2.0])


def test_04_large_scores_are_stable():
    np.testing.assert_allclose(solve([1000.0, 1000.0], [[0.0], [2.0]]), [1.0])
