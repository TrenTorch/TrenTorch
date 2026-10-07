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


def test_01_readme_example_1():
    _close(solve([3.0, 4.0]), np.array([0.6, 0.8]))


def test_02_readme_example_2():
    with pytest.raises(ValueError):
        solve([0.0, 0.0])


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([0, 0])


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([])


def test_05_random_valid_case_1():
    _close(solve([0.14, 3.64]), np.array([0.03843312210120439, 0.9992611746313143]))


def test_06_random_valid_case_2():
    _close(solve([-2.96, -0.25]), np.array([-0.9964522691492067, -0.0841598200294938]))


def test_07_random_valid_case_3():
    _close(solve([-0.97, 0.1, -2.28]), np.array([-0.39116401369469583, 0.040326186978834624, -0.9194370631174293]))


def test_08_random_valid_case_4():
    _close(solve([-1.6, -2.44, -0.97]), np.array([-0.5203561593280485, -0.7935431429752737, -0.3154659215926293]))


def test_09_random_valid_case_5():
    _close(solve([-4.62, -0.84, 2.48]), np.array([-0.8699901614925798, -0.15818002936228723, 0.4670077057362766]))


def test_10_random_valid_case_6():
    _close(solve([-0.58, -1.6, 4.69, -3.0]), np.array([-0.09962680232663693, -0.2748325581424467, 0.805602936055047, -0.5153110465170876]))


def test_11_random_valid_case_7():
    _close(solve([-0.16, 3.05, 3.97, -4.83]), np.array([-0.022994131362145103, 0.438325629090891, 0.5705418844232254, -0.6941353404947553]))


def test_12_random_valid_case_8():
    _close(solve([0.35, 3.15, -0.46, -4.56]), np.array([0.06281101961719347, 0.5652991765547413, -0.08255162578259714, -0.8183378555840063]))
