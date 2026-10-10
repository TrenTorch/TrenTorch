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
    _close(solve(1, 1), (1.0, 1.0))


def test_02_parameter_nudge():
    _close(solve(2, 2), (0.0, 0.0))


def test_03_random_valid_case():
    _close(solve([0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]), (0.5, 0.75))


def test_04_random_valid_case():
    _close(solve([1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]), (0.6666666666666666, 0.18181818181818182))


def test_05_random_valid_case():
    _close(solve([0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0]), (0.4444444444444444, 0.5))


def test_06_random_valid_case():
    _close(solve([0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0], [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1]), (0.14285714285714285, 0.25))


def test_07_random_valid_case():
    _close(solve([1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0], [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1]), (0.6, 0.75))


def test_08_random_valid_case():
    _close(solve([0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]), (1.0, 0.3))


def test_09_random_valid_case():
    _close(solve([1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]), (0.5, 0.3333333333333333))


def test_10_random_valid_case():
    _close(solve([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0], [0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]), (0.8571428571428571, 0.5454545454545454))


def test_11_random_valid_case():
    _close(solve([0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]), (0.14285714285714285, 0.2))


def test_12_random_valid_case():
    _close(solve([0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]), (0.8, 0.4444444444444444))
