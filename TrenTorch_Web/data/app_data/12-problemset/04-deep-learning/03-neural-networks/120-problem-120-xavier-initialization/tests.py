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
    _close(solve(2, 3, 0), np.array([[0.30006802263971943, -0.5043720396356872, -1.0056766217290054], [-1.0592348798055353, 0.6863407064201135, 0.9043021616442999]]))


def test_02_parameter_nudge():
    _close(solve(3, 4, 1), np.array([[0.021889395518930654, 0.8340966885527794, -0.6588883657100241, 0.8307373518230063], [-0.348420447747417, -0.14197182932425167, 0.6067872962131307, -0.1681305292522739], [0.09182966573912132, -0.8747905378278702, 0.46941506313391823, 0.07062769210065567]]))


def test_03_shape_and_bound():
    w = solve(200, 150, 5)
    a = np.sqrt(6 / (200 + 150))
    assert w.shape == (200, 150)
    assert np.abs(w).max() <= a


def test_04_uniform_distribution_statistics():
    w = solve(200, 150, 5)
    a = np.sqrt(6 / (200 + 150))
    assert abs(w.mean()) < 0.003
    assert w.std() == pytest.approx(a / np.sqrt(3), rel=0.03)
    assert w.max() > 0.95 * a and w.min() < -0.95 * a


def test_05_same_seed_is_reproducible():
    np.testing.assert_array_equal(solve(10, 7, 3), solve(10, 7, 3))


def test_06_different_seed_changes_values():
    assert not np.allclose(solve(10, 7, 3), solve(10, 7, 4))


def test_07_default_seed_is_zero():
    np.testing.assert_array_equal(solve(4, 5), solve(4, 5, 0))


def test_08_bound_shrinks_with_layer_width():
    assert np.abs(solve(10, 10, 0)).max() > np.abs(solve(1000, 1000, 0)).max()


def test_09_single_weight_is_within_bound():
    w = solve(1, 1, 7)
    assert w.shape == (1, 1)
    assert abs(w[0, 0]) <= np.sqrt(6 / 2)
