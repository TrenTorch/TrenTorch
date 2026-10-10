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
    _close(solve(['a', 'b', 'a'], ['a', 'b', 'c']), np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0]]))


def test_02_singleton_boundary():
    _close(solve(['a'], ['a']), np.array([[1]]))


def test_03_reversed_order():
    _close(solve(['a', 'b', 'a'], ['c', 'b', 'a']), np.array([[0, 0, 1], [0, 1, 0], [0, 0, 1]]))


def test_04_empty_or_degenerate_input():
    assert np.asarray(solve([], ['a', 'b', 'c'])).size == 0


def test_05_random_valid_case():
    _close(solve(['b', 'c', 'd', 'c', 'b', 'a', 'a'], ['a', 'b', 'c', 'd']), np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]))


def test_06_random_valid_case():
    _close(solve(['b', 'b', 'c', 'b', 'd', 'a', 'b'], ['a', 'b', 'c', 'd']), np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]))


def test_07_random_valid_case():
    _close(solve(['d', 'a', 'c', 'b', 'c', 'a', 'b'], ['a', 'b', 'c', 'd']), np.array([[0, 0, 0, 1], [1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]))


def test_08_random_valid_case():
    _close(solve(['b', 'a', 'a', 'a', 'b', 'b', 'a'], ['a', 'b', 'c', 'd']), np.array([[0, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0]]))


def test_09_random_valid_case():
    _close(solve(['b', 'c', 'a', 'c', 'd', 'a', 'b'], ['a', 'b', 'c', 'd']), np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]))


def test_10_random_valid_case():
    _close(solve(['c', 'd', 'b', 'd', 'a', 'a', 'b'], ['a', 'b', 'c', 'd']), np.array([[0, 0, 1, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0]]))


def test_11_random_valid_case():
    _close(solve(['d', 'a', 'a', 'd', 'a', 'c', 'a'], ['a', 'b', 'c', 'd']), np.array([[0, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0]]))


def test_12_random_valid_case():
    _close(solve(['a', 'a', 'd', 'b', 'b', 'd', 'b'], ['a', 'b', 'c', 'd']), np.array([[1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0]]))
