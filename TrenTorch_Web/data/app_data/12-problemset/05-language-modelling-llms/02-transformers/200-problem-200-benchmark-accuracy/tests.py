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
    _close(solve(['cat', 'dog', 'yes'], ['cat', 'cat', 'yes']), 0.6666666666666666)


def test_02_singleton_boundary():
    _close(solve(['cat'], ['cat']), 1.0)


def test_03_reversed_order():
    _close(solve(['yes', 'dog', 'cat'], ['yes', 'cat', 'cat']), 0.6666666666666666)


def test_04_random_valid_case():
    _close(solve(['no', 'cat', 'cat', 'dog', 'cat', ' no', 'no', ' dog'], ['cat', 'yes', 'no', 'dog', 'no ', 'dog', 'no', 'yes']), 0.25)


def test_05_random_valid_case():
    _close(solve([' no', 'yes', 'yes', ' yes', ' no', ' no', 'yes', 'yes'], ['yes ', 'yes ', 'yes', 'yes', 'yes', 'no', 'no', 'no']), 0.5)


def test_06_random_valid_case():
    _close(solve(['cat', ' dog', 'no', 'no', ' cat', 'no', ' yes', 'cat'], ['dog', 'yes', 'yes', 'no', 'cat', 'yes ', 'no ', 'cat']), 0.375)


def test_07_random_valid_case():
    _close(solve([' no', 'cat', 'no', 'no', ' no', ' yes', 'yes', ' dog'], ['cat', 'no', 'yes ', 'no', 'cat ', 'dog ', 'yes', 'cat']), 0.25)


def test_08_random_valid_case():
    _close(solve(['yes', ' dog', 'dog', ' cat', 'no', ' cat', 'yes', 'dog'], ['no ', 'cat ', 'yes', 'cat', 'yes', 'no', 'no', 'dog ']), 0.25)


def test_09_random_valid_case():
    _close(solve([' yes', 'cat', 'dog', ' cat', 'no', 'cat', 'dog', ' no'], ['yes ', 'no ', 'dog ', 'yes', 'dog', 'cat', 'no', 'yes']), 0.375)


def test_10_random_valid_case():
    _close(solve([' yes', 'yes', 'no', 'cat', 'cat', ' no', ' dog', ' dog'], ['yes', 'dog ', 'no', 'dog ', 'dog', 'dog', 'yes ', 'no']), 0.25)


def test_11_random_valid_case():
    _close(solve(['no', 'yes', 'dog', 'dog', 'cat', 'cat', ' cat', ' dog'], ['dog ', 'dog', 'cat ', 'no', 'yes', 'dog ', 'cat', 'yes']), 0.125)


def test_12_random_valid_case():
    _close(solve([' yes', 'dog', ' no', 'yes', ' yes', ' cat', ' dog', 'no'], ['dog', 'dog', 'no ', 'cat', 'cat ', 'no', 'cat', 'dog']), 0.25)
