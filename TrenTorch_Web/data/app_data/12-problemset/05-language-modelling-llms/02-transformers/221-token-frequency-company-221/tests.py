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
    _close(solve(['a', 'b', 'a']), {'a': 2, 'b': 1})


def test_02_singleton_boundary():
    _close(solve(['a']), {'a': 1})


def test_03_empty_or_degenerate_input():
    _close(solve([]), {})


def test_04_random_valid_case():
    _close(solve(['b', 'd', 'a', 'd', 'd', 'd', 'c', 'd', 'd', 'a', 'd', 'b', 'b', 'b']), {'b': 4, 'd': 7, 'a': 2, 'c': 1})


def test_05_random_valid_case():
    _close(solve(['c', 'c', 'd', 'b', 'a', 'c', 'b', 'c', 'a', 'b', 'b', 'a', 'a', 'a']), {'c': 4, 'd': 1, 'b': 4, 'a': 5})


def test_06_random_valid_case():
    _close(solve(['a', 'c', 'c', 'a', 'd', 'b', 'b', 'b', 'c', 'a', 'b', 'b', 'b', 'd']), {'a': 3, 'c': 3, 'd': 2, 'b': 6})


def test_07_random_valid_case():
    _close(solve(['b', 'a', 'a', 'a', 'd', 'd', 'd', 'c', 'b', 'a', 'd', 'b', 'a', 'a']), {'b': 3, 'a': 6, 'd': 4, 'c': 1})


def test_08_random_valid_case():
    _close(solve(['b', 'd', 'b', 'c', 'd', 'a', 'a', 'c', 'b', 'b', 'a', 'd', 'c', 'b']), {'b': 5, 'd': 3, 'c': 3, 'a': 3})


def test_09_random_valid_case():
    _close(solve(['d', 'd', 'c', 'a', 'a', 'a', 'c', 'd', 'c', 'b', 'd', 'c', 'a', 'd']), {'d': 5, 'c': 4, 'a': 4, 'b': 1})


def test_10_random_valid_case():
    _close(solve(['c', 'c', 'b', 'b', 'c', 'd', 'a', 'a', 'a', 'd', 'a', 'b', 'c', 'b']), {'c': 4, 'b': 4, 'd': 2, 'a': 4})


def test_11_random_valid_case():
    _close(solve(['b', 'b', 'b', 'd', 'b', 'c', 'a', 'a', 'b', 'c', 'c', 'c', 'b', 'a']), {'b': 6, 'd': 1, 'c': 4, 'a': 3})


def test_12_random_valid_case():
    _close(solve(['c', 'd', 'a', 'a', 'c', 'a', 'd', 'd', 'c', 'd', 'a', 'd', 'a', 'a']), {'c': 3, 'd': 5, 'a': 6})
