"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_symmetric_components_share_responsibility():
    out = solve([0.0], [0.5, 0.5], [[1.0], [-1.0]], [[[1.0]], [[1.0]]])
    np.testing.assert_allclose(out, [0.5, 0.5], atol=1e-9)


def test_02_point_near_first_mean_prefers_it():
    out = solve([1.0], [0.5, 0.5], [[1.0], [-1.0]], [[[1.0]], [[1.0]]])
    np.testing.assert_allclose(out, [1 / (1 + np.exp(-2.0)), 1 / (1 + np.exp(2.0))], atol=1e-9)


def test_03_weights_shift_responsibility():
    out = solve([0.0], [0.9, 0.1], [[1.0], [-1.0]], [[[1.0]], [[1.0]]])
    np.testing.assert_allclose(out, [0.9, 0.1], atol=1e-9)


def test_04_responsibilities_sum_to_one():
    out = solve([0.3, 0.7], [0.2, 0.8], [[0.0, 0.0], [1.0, 1.0]], [np.eye(2), np.eye(2)])
    assert abs(np.sum(out) - 1.0) < 1e-12
