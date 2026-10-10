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
    _close(solve(0.2, 0.8, 0.1), 2 / 3)


def test_02_zero_prior_stays_zero():
    _close(solve(0.0, 0.9, 0.1), 0.0)


def test_03_certain_prior_stays_one():
    _close(solve(1.0, 0.3, 0.9), 1.0)


def test_04_uninformative_evidence_keeps_prior():
    _close(solve(0.3, 0.5, 0.5), 0.3)


def test_05_impossible_under_h1():
    _close(solve(0.5, 0.0, 0.4), 0.0)


def test_06_impossible_under_h0():
    _close(solve(0.5, 0.4, 0.0), 1.0)


def test_07_rare_disease_test():
    _close(solve(0.01, 0.99, 0.05), 1 / 6)


def test_08_strong_evidence():
    _close(solve(0.5, 0.9, 0.3), 0.75)


def test_09_posterior_below_prior_when_h0_likelier():
    _close(solve(0.6, 0.2, 0.8), 0.12 / (0.12 + 0.32))


def test_10_prior_above_one_raises():
    with pytest.raises(ValueError):
        solve(1.2, 0.5, 0.5)


def test_11_negative_likelihood_raises():
    with pytest.raises(ValueError):
        solve(0.5, -0.1, 0.5)


def test_12_zero_evidence_raises():
    with pytest.raises(ValueError):
        solve(0.5, 0.0, 0.0)


def test_13_zero_evidence_certain_prior_raises():
    with pytest.raises(ValueError):
        solve(1.0, 0.0, 0.5)
