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
    _close(solve(6, 0), np.array([5, 3, 3, 1, 1, 0]))


def test_02_parameter_nudge():
    _close(solve(7, 1), np.array([3, 3, 5, 6, 0, 1, 5]))


def test_03_random_valid_case():
    _close(solve(5, 7), np.array([4, 3, 3, 4, 2]))


def test_04_random_valid_case():
    _close(solve(8, 7), np.array([7, 5, 5, 7, 4, 6, 6, 1]))


def test_05_random_valid_case():
    _close(solve(9, 7), np.array([8, 5, 6, 8, 5, 6, 7, 2, 0]))


def test_06_random_valid_case():
    _close(solve(10, 7), np.array([9, 6, 6, 8, 5, 7, 8, 2, 0, 3]))


def test_07_random_valid_case():
    _close(solve(23, 7), np.array([21, 14, 15, 20, 13, 17, 19, 5, 1, 6, 6, 20, 20, 0, 11, 18, 3, 18, 2, 10, 18, 6, 7]))


def test_08_random_valid_case():
    _close(solve(17, 7), np.array([16, 10, 11, 15, 9, 13, 14, 3, 0, 5, 4, 14, 15, 0, 8, 13, 2]))


def test_09_random_valid_case():
    _close(solve(38, 7), np.array([35, 23, 25, 34, 21, 29, 31, 8, 2, 11, 10, 33, 34, 0, 18, 31, 4, 30, 4, 17, 31, 11, 12, 10, 27, 9, 37, 16, 18, 19, 22, 21, 19, 37, 30, 30, 26, 23]))


def test_10_random_valid_case():
    _close(solve(29, 7), np.array([27, 18, 19, 26, 16, 22, 24, 6, 1, 8, 8, 25, 26, 0, 14, 23, 3, 23, 3, 13, 23, 8, 9, 8, 20, 7, 28, 12, 13]))


def test_11_random_valid_case():
    _close(solve(22, 7), np.array([20, 13, 15, 19, 12, 17, 18, 4, 1, 6, 6, 19, 20, 0, 10, 18, 2, 17, 2, 10, 17, 6]))


def test_12_random_valid_case():
    _close(solve(36, 7), np.array([34, 22, 24, 32, 20, 27, 30, 8, 1, 10, 10, 31, 32, 0, 17, 29, 4, 28, 4, 16, 29, 10, 12, 10, 25, 9, 35, 16, 17, 18, 20, 19, 18, 35, 29, 28]))
