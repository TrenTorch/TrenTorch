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
    _close(solve([10.0, 20.0, 30.0]), np.array([0.0, 0.5, 1.0]))


def test_02_readme_example_2():
    _close(solve([5.0, 5.0, 5.0]), np.array([0.0, 0.0, 0.0]))


def test_03_readme_example_3():
    _close(solve([-1.0, 0.0, 3.0]), np.array([0.0, 0.25, 1.0]))


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve(np.array([]))


def test_05_random_valid_case_1():
    _close(solve([3.0, 3.0]), np.array([0.0, 0.0]))


def test_06_random_valid_case_2():
    _close(solve([2.53, -1.07, 4.76, 4.57, 0.83, 3.83, 2.73]), np.array([0.6174957118353344, 0.0, 1.0, 0.9674099485420241, 0.3259005145797598, 0.8404802744425387, 0.6518010291595197]))


def test_07_random_valid_case_3():
    _close(solve([3.77, -4.6, -3.94, 0.74, 1.8, -4.36, 4.73]), np.array([0.8971061093247588, 0.0, 0.07073954983922827, 0.5723472668810289, 0.6859592711682744, 0.025723472668810216, 1.0]))


def test_08_random_valid_case_4():
    _close(solve([4.89, 2.29, 4.61, 0.29, -3.2, -1.43, 2.26]), np.array([1.0, 0.6786155747836836, 0.9653893695920891, 0.4313967861557479, 0.0, 0.21878862793572315, 0.6749072929542645]))


def test_09_random_valid_case_5():
    _close(solve([-4.09, 2.84, 2.59, 2.04, -0.5, 4.75, 4.79]), np.array([0.0, 0.7804054054054055, 0.7522522522522523, 0.6903153153153154, 0.4042792792792793, 0.9954954954954955, 1.0]))


def test_10_random_valid_case_6():
    _close(solve([2.27, 4.53, 1.98, -1.81, 3.89, -3.7, -1.67]), np.array([0.7253948967193196, 1.0, 0.6901579586877278, 0.22964763061968407, 0.922235722964763, 0.0, 0.24665856622114218]))


def test_11_random_valid_case_7():
    _close(solve([-2.75, -0.96, 2.67, -0.76, 3.1, 0.05, -1.6]), np.array([0.0, 0.305982905982906, 0.9264957264957265, 0.3401709401709402, 1.0, 0.47863247863247865, 0.19658119658119658]))


def test_12_random_valid_case_8():
    _close(solve([-3.89, 2.16, 3.18, 2.71, 1.73, 0.49, -2.23]), np.array([0.0, 0.8557284299858557, 1.0, 0.9335219236209334, 0.7949080622347949, 0.6195190947666195, 0.2347949080622348]))
