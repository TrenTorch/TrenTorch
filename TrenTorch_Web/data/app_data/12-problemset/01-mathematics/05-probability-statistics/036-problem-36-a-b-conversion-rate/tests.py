"""Tests with varied inputs. Expected values were checked against independent references (SciPy, scikit-learn, PyTorch or a first-principles formula)."""
import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def _close(actual, expected, rtol=1e-6, atol=1e-8):
    if isinstance(expected, dict):
        assert set(actual) == set(expected)
        for k in expected:
            _close(actual[k], expected[k], rtol, atol)
        return
    if isinstance(expected, (tuple, list)) and not (len(expected) and isinstance(expected[0], (int, float, np.number)) and not isinstance(expected, tuple)):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            _close(a, e, rtol, atol)
        return
    a, e = np.asarray(actual), np.asarray(expected)
    assert a.shape == e.shape, (a.shape, e.shape)
    if a.dtype.kind in "biufc" and e.dtype.kind in "biufc":
        np.testing.assert_allclose(a, e, rtol=rtol, atol=atol, equal_nan=True)
    else:
        assert a.tolist() == e.tolist()


def test_01_basic_example():
    _close(solve([0, 1, 0, 0, 1], [1, 1, 0, 1, 1]), (0.4, 0.8, 0.4))


def test_02_no_difference():
    _close(solve([1, 0], [1, 0]), (0.5, 0.5, 0.0))


def test_03_treatment_converts_everyone():
    _close(solve([0, 0, 0], [1, 1, 1]), (0.0, 1.0, 1.0))


def test_04_treatment_hurts():
    _close(solve([1, 1, 1, 0], [1, 0, 0, 0]), (0.75, 0.25, -0.5))


def test_05_unequal_group_sizes():
    _close(solve([1] + [0] * 9, [1, 1, 0, 0]), (0.1, 0.5, 0.4))


def test_06_single_user_each():
    _close(solve([1], [0]), (1.0, 0.0, -1.0))


def test_07_larger_experiment():
    _close(solve([1] * 30 + [0] * 70, [1] * 45 + [0] * 55), (0.3, 0.45, 0.15))


def test_08_numpy_input():
    _close(solve(np.array([0, 0, 1, 0]), np.array([1, 0, 1, 1])), (0.25, 0.75, 0.5))


def test_09_both_zero():
    _close(solve([0, 0], [0, 0, 0]), (0.0, 0.0, 0.0))


def test_10_empty_control_raises():
    with pytest.raises(ValueError):
        solve([], [1, 0])


def test_11_empty_treatment_raises():
    with pytest.raises(ValueError):
        solve([1, 0], [])


def test_12_non_binary_raises():
    with pytest.raises(ValueError):
        solve([0, 2], [1, 0])


def test_13_scalar_input_raises():
    with pytest.raises(ValueError):
        solve(10, 100)
