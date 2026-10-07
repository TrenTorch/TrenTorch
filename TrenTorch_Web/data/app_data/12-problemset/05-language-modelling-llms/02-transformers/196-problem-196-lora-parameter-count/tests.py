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
    _close(solve(10, 8, 2), 36)


def test_02_parameter_nudge():
    _close(solve(11, 9, 3), 60)


def test_03_random_valid_case():
    _close(solve(9, 9, 4), 72)


def test_04_random_valid_case():
    _close(solve(27, 8, 4), 140)


def test_05_random_valid_case():
    _close(solve(97, 4, 7), 707)


def test_06_random_valid_case():
    _close(solve(9, 36, 5), 225)


def test_07_random_valid_case():
    _close(solve(42, 8, 3), 150)


def test_08_random_valid_case():
    _close(solve(40, 39, 6), 474)


def test_09_random_valid_case():
    _close(solve(13, 88, 2), 202)


def test_10_random_valid_case():
    _close(solve(34, 68, 5), 510)


def test_11_random_valid_case():
    _close(solve(89, 19, 4), 432)


def test_12_random_valid_case():
    _close(solve(89, 91, 6), 1080)
