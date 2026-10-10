"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve([1, -1], [1, 1], [0.5, 0.5], 0.25), [0.25, 0.75], atol=1e-9)


def test_02_zero_error_leaves_weights_unchanged():
    np.testing.assert_allclose(solve([1, 1], [1, -1], [1.0, 3.0], 0.5), [0.25, 0.75], atol=1e-9)


def test_03_all_negative_labels():
    np.testing.assert_allclose(solve([-1, -1], [-1, 1], [0.5, 0.5], 0.25), [0.25, 0.75], atol=1e-9)


def test_04_singleton_boundary():
    np.testing.assert_allclose(solve([1], [1], [1.0], 0.2), [1.0], atol=1e-9)


def test_05_repeated_values_stay_uniform():
    np.testing.assert_allclose(solve([1, 1, 1], [1, 1, 1], [1 / 3] * 3, 0.5), [1 / 3] * 3, atol=1e-9)


def test_06_result_sums_to_one():
    out = solve([1, -1, 1], [1, 1, -1], [0.2, 0.3, 0.5], 0.3)
    assert abs(out.sum() - 1.0) < 1e-12
