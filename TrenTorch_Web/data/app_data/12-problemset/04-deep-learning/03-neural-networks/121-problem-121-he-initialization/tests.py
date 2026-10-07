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
    _close(solve(2, 3, 0), np.array([[0.1257302210933933, -0.1321048632913019, 0.6404226504432821], [0.10490011715303971, -0.535669373161111, 0.36159505490948474]]))


def test_02_parameter_nudge():
    _close(solve(3, 4, 1), np.array([[0.2821683112435684, 0.6708484049968816, 0.2698007429154901, -1.0640234240162014], [0.7392199696614589, 0.36446331214829103, -0.4384204807897534, 0.4744809451915244], [0.29767211498655916, 0.24015817785897278, 0.023206662856650833, 0.4463892843178486]]))


def test_03_shape_and_zero_mean():
    w = solve(300, 100, 5)
    assert w.shape == (300, 100)
    assert abs(w.mean()) < 0.003


def test_04_standard_deviation_is_sqrt_two_over_fan_in():
    w = solve(300, 100, 5)
    assert w.std() == pytest.approx(np.sqrt(2 / 300), rel=0.03)


def test_05_std_ignores_fan_out():
    narrow = solve(200, 20, 1).std()
    wide = solve(200, 400, 1).std()
    assert narrow == pytest.approx(wide, rel=0.15)


def test_06_same_seed_is_reproducible():
    np.testing.assert_array_equal(solve(10, 7, 3), solve(10, 7, 3))


def test_07_different_seed_changes_values():
    assert not np.allclose(solve(10, 7, 3), solve(10, 7, 4))


def test_08_default_seed_is_zero():
    np.testing.assert_array_equal(solve(4, 5), solve(4, 5, 0))


def test_09_larger_fan_in_gives_smaller_weights():
    assert solve(10, 300, 0).std() > solve(1000, 300, 0).std()
