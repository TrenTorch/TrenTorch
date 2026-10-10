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
    _close(solve(1.7), 5.4739473917272)


def test_04_random_valid_case():
    _close(solve(5.4), 221.40641620418717)


def test_05_random_valid_case():
    _close(solve(5.3), 200.33680997479166)


def test_06_random_valid_case():
    _close(solve(2.99), 19.88568249156473)


def test_07_random_valid_case():
    _close(solve(1.99), 7.315533762309567)


def test_08_random_valid_case():
    _close(solve(4.96), 142.5937958969891)


def test_09_random_valid_case():
    _close(solve(3.17), 23.80748435642867)


def test_10_random_valid_case():
    _close(solve(2.58), 13.197138159658358)


def test_11_random_valid_case():
    _close(solve(3.46), 31.81697651466769)


def test_12_random_valid_case():
    _close(solve(1.91), 6.753088798531286)
