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
    _close(solve([['a', 'b'], ['a', 'c'], ['a', 'b']], ['a', 'b']), 0.6666666666666666)


def test_02_singleton_boundary():
    _close(solve([['a', 'b']], ['a']), 1.0)


def test_03_reversed_order():
    _close(solve([['a', 'b'], ['a', 'c'], ['a', 'b']], ['b', 'a']), 0.6666666666666666)


def test_04_empty_or_degenerate_input():
    _close(solve([['a', 'b'], ['a', 'c'], ['a', 'b']], []), 1.0)


def test_05_random_valid_case():
    _close(solve([[4], [2, 4], [4], [1, 5], [0, 3], [0, 2, 3], [2], [0, 4, 5], [0, 5], [1]], [1, 5]), 0.1)


def test_06_random_valid_case():
    _close(solve([[2, 4, 5], [0, 5], [4], [2], [1, 2, 3, 4], [0, 3], [3], [4], [4, 5], [4, 5]], [1, 2]), 0.1)


def test_07_random_valid_case():
    _close(solve([[3, 4], [1, 2, 3, 5], [0, 2, 5], [4], [1], [0, 1], [1], [1], [1, 2, 5], [4, 5]], [1, 4]), 0.0)


def test_08_random_valid_case():
    _close(solve([[5], [0], [2, 4], [3, 4], [2, 3, 4], [0, 5], [5], [0, 2, 4, 5], [0, 2], [1, 4]], [0, 1]), 0.0)


def test_09_random_valid_case():
    _close(solve([[0, 1, 3], [5], [0, 1, 2, 3], [1, 4], [0, 2, 4, 5], [0], [5], [0, 1, 3], [1], [3]], [5, 4]), 0.1)


def test_10_random_valid_case():
    _close(solve([[4], [0], [4], [0, 3, 4, 5], [2, 3, 4], [3, 4], [2], [2, 3, 4], [0, 4, 5], [0, 2, 4]], [4, 3]), 0.4)


def test_11_random_valid_case():
    _close(solve([[0, 5], [1, 3, 5], [0, 5], [1, 4, 5], [0, 3], [0, 1, 3], [0, 3, 4], [0, 3, 4], [3], [2]], [5, 3]), 0.1)


def test_12_random_valid_case():
    _close(solve([[1, 2, 3], [3, 5], [2], [2, 5], [0, 2, 3, 5], [5], [1, 4], [0, 2, 5], [3, 5], [0, 1, 2, 4]], [3, 1]), 0.1)
