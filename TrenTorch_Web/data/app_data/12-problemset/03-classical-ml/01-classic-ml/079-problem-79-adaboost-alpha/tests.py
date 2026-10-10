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
    _close(solve(0.2), 0.6931471805599453)


def test_02_parameter_nudge():
    with pytest.raises(ValueError):
        solve(1.2)


def test_03_random_valid_case():
    _close(solve(0.6), -0.20273255405408214)


def test_04_random_valid_case():
    _close(solve(0.9), -1.0986122886681098)


def test_05_random_valid_case():
    _close(solve(0.8), -0.6931471805599454)


def test_06_random_valid_case():
    _close(solve(0.4), 0.2027325540540821)


def test_07_random_valid_case():
    _close(solve(0.1), 1.0986122886681098)


def test_08_random_valid_case():
    _close(solve(0.48), 0.04002135383676828)


def test_09_random_valid_case():
    _close(solve(0.15), 0.8673005276940532)


def test_10_random_valid_case():
    _close(solve(0.99), -2.2975599250672945)


def test_11_random_valid_case():
    _close(solve(0.88), -0.9962150823451031)


def test_12_random_valid_case():
    _close(solve(0.43), 0.1409255760704939)
