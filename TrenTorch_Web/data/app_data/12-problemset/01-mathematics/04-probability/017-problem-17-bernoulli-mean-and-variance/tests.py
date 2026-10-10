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
    _close(solve([0, 1, 1, 0, 1]), (0.6, 0.24))


def test_02_all_zeros():
    _close(solve([0, 0, 0, 0]), (0.0, 0.0))


def test_03_all_ones():
    _close(solve([1, 1, 1]), (1.0, 0.0))


def test_04_single_observation():
    _close(solve([1]), (1.0, 0.0))


def test_05_balanced_gives_max_variance():
    _close(solve([0, 1, 0, 1]), (0.5, 0.25))


def test_06_rare_event():
    _close(solve([1] * 3 + [0] * 7), (0.3, 0.21))


def test_07_float_encoded_labels():
    _close(solve([1.0, 0.0, 0.0, 0.0]), (0.25, 0.1875))


def test_08_numpy_input():
    _close(solve(np.array([1, 0, 1, 1, 0, 0, 1, 1])), (0.625, 0.234375))


def test_09_order_does_not_matter():
    _close(solve([1, 1, 0, 0, 0, 1]), (0.5, 0.25))


def test_10_empty_raises():
    with pytest.raises(ValueError):
        solve([])


def test_11_non_binary_raises():
    with pytest.raises(ValueError):
        solve([0, 2, 1])


def test_12_fractional_raises():
    with pytest.raises(ValueError):
        solve([0.5, 1])


def test_13_two_dimensional_raises():
    with pytest.raises(ValueError):
        solve([[0, 1], [1, 0]])
