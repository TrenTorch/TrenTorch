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
    _close(solve(1, 1, 1, 1), 1.0)


def test_02_parameter_nudge():
    _close(solve(2, 2, 2, 2), 2.0)


def test_03_random_valid_case():
    _close(solve(0, 9, 0.7, 0.23), 0.7)


def test_04_random_valid_case():
    _close(solve(3, 18, 0.8, 0.35), 0.7698557158514987)


def test_05_random_valid_case():
    _close(solve(6, 16, 0.59, 0.3), 0.500489097692938)


def test_06_random_valid_case():
    _close(solve(3, 7, 1.87, 0.24), 1.2363545611743962)


def test_07_random_valid_case():
    _close(solve(6, 18, 1.4, 0.21), 1.1025)


def test_08_random_valid_case():
    _close(solve(5, 32, 1.74, 0.33), 1.6567544913655903)


def test_09_random_valid_case():
    _close(solve(34, 34, 1.63, 0.2), 0.2)


def test_10_random_valid_case():
    _close(solve(9, 11, 1.36, 0.22), 0.3104854862862268)


def test_11_random_valid_case():
    _close(solve(2, 39, 1.96, 0.22), 1.948733728494984)


def test_12_random_valid_case():
    _close(solve(14, 34, 1.04, 0.3), 0.7712553063266707)
