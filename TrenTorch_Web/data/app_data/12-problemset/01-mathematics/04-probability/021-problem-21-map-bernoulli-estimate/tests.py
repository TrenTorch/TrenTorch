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
    _close(solve([1, 1, 0, 1], 1.0, 1.0), 0.75)


def test_02_informative_prior_pulls_toward_half():
    _close(solve([1, 1, 0, 1], 2.0, 2.0), 4 / 6)


def test_03_no_successes():
    _close(solve([0, 0, 0], 1.0, 1.0), 0.0)


def test_04_all_successes():
    _close(solve([1, 1, 1], 1.0, 1.0), 1.0)


def test_05_no_data_returns_prior_mode():
    _close(solve([], 2.0, 2.0), 0.5)


def test_06_skewed_prior():
    _close(solve([1, 0, 0, 0, 0, 0], 3.0, 5.0), 3 / 12)


def test_07_fractional_prior():
    _close(solve([1] * 20 + [0] * 5, 1.5, 1.5), 20.5 / 26)


def test_08_numpy_input():
    _close(solve(np.array([0, 1, 0, 0]), 2.0, 3.0), 2 / 7)


def test_09_more_data_overrides_prior():
    _close(solve([1] * 90 + [0] * 10, 2.0, 8.0), 91 / 108)


def test_10_prior_below_one_raises():
    with pytest.raises(ValueError):
        solve([1, 0], 0.5, 1.0)


def test_11_non_binary_observation_raises():
    with pytest.raises(ValueError):
        solve([0, 2], 1.0, 1.0)


def test_12_uniform_prior_no_data_raises():
    with pytest.raises(ValueError):
        solve([], 1.0, 1.0)
