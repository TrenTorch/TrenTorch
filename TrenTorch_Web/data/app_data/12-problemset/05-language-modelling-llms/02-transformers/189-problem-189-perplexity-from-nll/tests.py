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
    _close(solve(1.0), 2.718281828459045)


def test_02_parameter_nudge():
    _close(solve(2.0), 7.38905609893065)


def test_03_random_valid_case():
    _close(solve(3.3), 27.112638920657883)


def test_04_random_valid_case():
    _close(solve(5.4), 221.40641620418717)


def test_05_random_valid_case():
    _close(solve(2.56), 12.935817315543076)


def test_06_random_valid_case():
    _close(solve(4.52), 91.83559797815674)


def test_07_random_valid_case():
    _close(solve(5.86), 350.7241440199136)


def test_08_random_valid_case():
    _close(solve(3.38), 29.370771113289432)


def test_09_random_valid_case():
    _close(solve(1.37), 3.9353506954704733)


def test_10_random_valid_case():
    _close(solve(2.52), 12.428596663577544)


def test_11_random_valid_case():
    _close(solve(3.67), 39.2519058603045)


def test_12_random_valid_case():
    _close(solve(3.52), 33.78442846384956)
