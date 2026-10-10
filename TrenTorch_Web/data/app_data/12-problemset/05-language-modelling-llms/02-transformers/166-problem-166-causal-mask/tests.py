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
    _close(solve(4), np.array([[True, False, False, False], [True, True, False, False], [True, True, True, False], [True, True, True, True]]))


def test_02_parameter_nudge():
    _close(solve(5), np.array([[True, False, False, False, False], [True, True, False, False, False], [True, True, True, False, False], [True, True, True, True, False], [True, True, True, True, True]]))


def test_03_random_valid_case():
    _close(solve(6), np.array([[True, False, False, False, False, False], [True, True, False, False, False, False], [True, True, True, False, False, False], [True, True, True, True, False, False], [True, True, True, True, True, False], [True, True, True, True, True, True]]))


def test_04_random_valid_case():
    _close(solve(2), np.array([[True, False], [True, True]]))


def test_05_random_valid_case():
    _close(solve(4), np.array([[True, False, False, False], [True, True, False, False], [True, True, True, False], [True, True, True, True]]))


def test_06_random_valid_case():
    _close(solve(7), np.array([[True, False, False, False, False, False, False], [True, True, False, False, False, False, False], [True, True, True, False, False, False, False], [True, True, True, True, False, False, False], [True, True, True, True, True, False, False], [True, True, True, True, True, True, False], [True, True, True, True, True, True, True]]))


def test_07_random_valid_case():
    _close(solve(3), np.array([[True, False, False], [True, True, False], [True, True, True]]))


def test_08_random_valid_case():
    _close(solve(1), np.array([[True]]))


def test_09_random_valid_case():
    _close(solve(5), np.array([[True, False, False, False, False], [True, True, False, False, False], [True, True, True, False, False], [True, True, True, True, False], [True, True, True, True, True]]))


def test_10_random_valid_case():
    _close(solve(8), np.array([[True, False, False, False, False, False, False, False], [True, True, False, False, False, False, False, False], [True, True, True, False, False, False, False, False], [True, True, True, True, False, False, False, False], [True, True, True, True, True, False, False, False], [True, True, True, True, True, True, False, False], [True, True, True, True, True, True, True, False], [True, True, True, True, True, True, True, True]]))
