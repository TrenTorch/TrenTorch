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


def test_01_textbook_ten_vs_twenty_percent():
    _close(solve(0.1, 0.2), 199)


def test_02_returns_int():
    out = solve(0.1, 0.2)
    assert isinstance(out, int) and out > 0


def test_03_symmetric_inputs():
    _close(solve(0.3, 0.2), solve(0.2, 0.3))


def test_04_smaller_effect_needs_more_samples():
    out = solve(0.4, 0.41)
    assert out > solve(0.4, 0.5)


def test_05_half_vs_fifty_five_percent():
    _close(solve(0.5, 0.55), 1563)


def test_06_five_vs_ten_percent():
    _close(solve(0.05, 0.1), 434)


def test_07_thirty_vs_fifty_percent():
    _close(solve(0.3, 0.5), 93)


def test_08_zero_baseline():
    _close(solve(0.0, 0.1), 74)


def test_09_equal_rates_raise():
    with pytest.raises(ValueError):
        solve(0.2, 0.2)


def test_10_negative_rate_raises():
    with pytest.raises(ValueError):
        solve(-0.1, 0.2)


def test_11_rate_above_one_raises():
    with pytest.raises(ValueError):
        solve(0.2, 1.5)
