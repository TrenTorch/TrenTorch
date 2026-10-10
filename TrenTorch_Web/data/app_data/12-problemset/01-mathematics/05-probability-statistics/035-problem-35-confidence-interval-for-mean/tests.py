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
    _close(solve([1.0, 2.0, 3.0, 4.0]), (1.2348254402389105, 3.7651745597610895))


def test_02_readme_example_2():
    _close(solve([10.0, 12.0, 11.0, 13.0, 9.0], critical=2.576), (9.178492931663452, 12.821507068336548))


def test_03_random_valid_case_1():
    _close(solve([1.8, 4.49, -3.49, -0.18, 4.7, 2.41, 2.71, 4.3, 4.61, 3.63, -0.03, -0.7], 1.96), (0.5408741222178186, 3.5007925444488484))


def test_04_random_valid_case_2():
    _close(solve([2.03, -1.87, -2.39, 3.73, 1.84, 1.09, 3.97, 0.8, 1.57, 4.74, 3.42, 1.95], 1.96), (0.5060629277869078, 2.9739370722130922))


def test_05_random_valid_case_3():
    _close(solve([-2.52, 4.7, -4.83, 0.89, -2.14, -4.96, 2.43, -1.45, 1.91, 0.2, 0.68, 1.79], 1.96), (-1.948208629060834, 1.3982086290608342))


def test_06_random_valid_case_4():
    _close(solve([4.05, 2.85, 4.48, -4.8, 4.42, -3.45, -4.66, -1.64, 0.13, 3.82, 2.11, 3.53], 1.96), (-1.152400435736224, 2.9590671024028907))


def test_07_random_valid_case_5():
    _close(solve([-2.18, 4.69, 3.72, -4.29, 2.48, 0.5, -4.45, 2.76, 3.48, 3.24, 3.38, -1.33], 1.96), (-0.8422230733874801, 2.84222307338748))


def test_08_random_valid_case_6():
    _close(solve([4.88, 2.71, 3.59, 4.7, -1.08, 3.82, -4.87, -4.68, 4.26, 0.97, 0.86, -2.98], 1.96), (-1.0311614039242094, 3.061161403924209))


def test_09_random_valid_case_7():
    _close(solve([2.35, 4.34, 4.74, 2.17, -4.85, 1.56, -0.51, 0.12, -1.66, 4.36, 0.47, -2.64], 1.96), (-0.8147104803297162, 2.556377146996383))


def test_10_random_valid_case_8():
    _close(solve([-4.74, 2.66, 1.83, -2.9, -4.24, 4.73, 1.28, 0.71, 4.57, -0.34, -1.35, 3.09], 1.96), (-1.378405610841437, 2.2617389441747706))


def test_11_random_valid_case_9():
    _close(solve([3.32, 3.42, -3.78, -4.23, 4.47, 1.09, 1.57, -0.47, 3.6, 2.53, -4.99, -1.24], 1.96), (-1.4451719094103253, 2.326838576076992))


def test_12_random_valid_case_10():
    _close(solve([-2.66, -3.4, 2.35, -0.23, 0.77, 3.91, 1.71, -4.67, 4.81, 2.67, 1.04, -0.18], 1.96), (-1.1359014396648752, 2.1559014396648752))
