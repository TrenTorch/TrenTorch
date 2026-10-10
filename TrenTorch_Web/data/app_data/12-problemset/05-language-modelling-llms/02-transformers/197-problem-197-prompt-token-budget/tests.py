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
    _close(solve(10, 6), 4)


def test_02_parameter_nudge():
    _close(solve(11, 7), 4)


def test_03_random_valid_case():
    _close(solve(1761, 78), 1683)


def test_04_random_valid_case():
    _close(solve(223, 721), 0)


def test_05_random_valid_case():
    _close(solve(4188, 323), 3865)


def test_06_random_valid_case():
    _close(solve(972, 4946), 0)


def test_07_random_valid_case():
    _close(solve(608, 5630), 0)


def test_08_random_valid_case():
    _close(solve(2036, 1952), 84)


def test_09_random_valid_case():
    _close(solve(4884, 3483), 1401)


def test_10_random_valid_case():
    _close(solve(4633, 4707), 0)


def test_11_random_valid_case():
    _close(solve(3063, 2188), 875)


def test_12_random_valid_case():
    _close(solve(2023, 1187), 836)
