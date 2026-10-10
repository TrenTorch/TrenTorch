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
    _close(solve(1, 1), 0.0)


def test_02_parameter_nudge():
    _close(solve(2, 2), 0.0)


def test_03_random_valid_case():
    _close(solve(2.9, 0.81), 2.09)


def test_04_random_valid_case():
    _close(solve(2.46, 0.5), 1.96)


def test_05_random_valid_case():
    _close(solve(1.93, 1.17), 0.76)


def test_06_random_valid_case():
    _close(solve(2.06, 0.59), 1.4700000000000002)


def test_07_random_valid_case():
    _close(solve(0.96, 0.25), 0.71)


def test_08_random_valid_case():
    _close(solve(3.32, 1.31), 2.01)


def test_09_random_valid_case():
    _close(solve(3.77, 0.37), 3.4)


def test_10_random_valid_case():
    _close(solve(1.15, 0.86), 0.2899999999999999)


def test_11_random_valid_case():
    _close(solve(0.34, 1.12), 0.0)


def test_12_random_valid_case():
    _close(solve(1.62, 0.18), 1.4400000000000002)
