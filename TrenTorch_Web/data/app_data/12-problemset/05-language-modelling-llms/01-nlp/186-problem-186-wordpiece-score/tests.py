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
    _close(solve(2.0, 3.0, 1.0), 0.6666666666666666)


def test_02_parameter_nudge():
    _close(solve(3.0, 4.0, 2.0), 0.375)


def test_03_random_valid_case():
    _close(solve(9, 7, 7), 0.1836734693877551)


def test_04_random_valid_case():
    _close(solve(9, 8, 29), 0.03879310344827586)


def test_05_random_valid_case():
    _close(solve(4, 9, 12), 0.037037037037037035)


def test_06_random_valid_case():
    _close(solve(6, 17, 5), 0.07058823529411765)


def test_07_random_valid_case():
    _close(solve(2, 8, 27), 0.009259259259259259)


def test_08_random_valid_case():
    _close(solve(12, 3, 27), 0.14814814814814814)


def test_09_random_valid_case():
    _close(solve(19, 1, 17), 1.1176470588235294)


def test_10_random_valid_case():
    _close(solve(1, 16, 25), 0.0025)


def test_11_random_valid_case():
    _close(solve(18, 29, 9), 0.06896551724137931)


def test_12_random_valid_case():
    _close(solve(3, 23, 26), 0.005016722408026756)
