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
    _close(solve(5, 0.1, 0.01), 4.886186104779053)


def test_02_parameter_nudge():
    _close(solve(6, 1.1, 1.01), 6.606293470549717)


def test_03_random_valid_case():
    _close(solve(0.1, 0.9, 18), 0.015009463529699918)


def test_04_random_valid_case():
    _close(solve(0.63, 0.9, 11), 0.19770067553670004)


def test_05_random_valid_case():
    _close(solve(1.62, 0.78, 2), 0.9856080000000002)


def test_06_random_valid_case():
    _close(solve(1.55, 0.66, 1), 1.0230000000000001)


def test_07_random_valid_case():
    _close(solve(0.53, 0.97, 3), 0.48371669)


def test_08_random_valid_case():
    _close(solve(1.83, 0.59, 7), 0.04554232217218769)


def test_09_random_valid_case():
    _close(solve(1.57, 0.58, 3), 0.30632583999999996)


def test_10_random_valid_case():
    _close(solve(1.63, 0.77, 19), 0.011363480804964004)


def test_11_random_valid_case():
    _close(solve(1.24, 0.83, 11), 0.15969109589872255)


def test_12_random_valid_case():
    _close(solve(0.22, 0.72, 16), 0.0011474733919031833)
