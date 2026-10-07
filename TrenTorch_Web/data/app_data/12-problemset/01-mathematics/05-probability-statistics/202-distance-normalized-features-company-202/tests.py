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
    _close(solve([0.0, 0.0]), np.array([0.0, 0.0]))


def test_03_random_valid_case_1():
    _close(solve([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]))


def test_04_random_valid_case_2():
    _close(solve([3.4, -4.05, 2.0, 3.65, 1.51]), np.array([0.49298614050571077, -0.5872334908965084, 0.28999184735630046, 0.5292351214252483, 0.21894384475400686]))


def test_05_random_valid_case_3():
    _close(solve([0.27, 3.64, 4.03, 4.47, 0.93]), np.array([0.03802847076867008, 0.5126801244368855, 0.5676101377694089, 0.6295824605035379, 0.13098695486986361]))


def test_06_random_valid_case_4():
    _close(solve([4.04, 4.1, 3.1, -2.45, -1.05]), np.array([0.572220740111164, 0.580719067934597, 0.4390802708773783, -0.3470150527901861, -0.14872073691007973]))


def test_07_random_valid_case_5():
    _close(solve([4.87, 1.58, -3.3, 1.34, -2.6]), np.array([0.7207194442399191, 0.23382684227907027, -0.48837251868413406, 0.19830884092022416, -0.3847783480541663]))


def test_08_random_valid_case_6():
    _close(solve([3.09, 0.56, 1.09, 4.65, -0.05]), np.array([0.5405700876712425, 0.09796739452941612, 0.19068653578047065, 0.8134792581460446, -0.008747088797269296]))


def test_09_random_valid_case_7():
    _close(solve([0.39, 0.29, -3.04, -1.9, 3.12]), np.array([0.08163677756609634, 0.06070427049786651, -0.6363482148741869, -0.3977176342963668, 0.6530942205287708]))


def test_10_random_valid_case_8():
    _close(solve([0.06, 2.88, 4.91, -0.56, 0.18]), np.array([0.010484112553467796, 0.5032374025664542, 0.8579498772921147, -0.09785171716569943, 0.03145233766040339]))


def test_11_random_valid_case_9():
    _close(solve([2.61, -3.19, 2.8, 2.78, -0.42]), np.array([0.4561919339060061, -0.5575679192184518, 0.4894013084049107, 0.4859055847734471, -0.07341019626073661]))


def test_12_random_valid_case_10():
    _close(solve([3.39, -0.04, 4.09, -4.7, -1.91]), np.array([0.4614919502987554, -0.005445332746887969, 0.5567852733692948, -0.6398265977593364, -0.2600146386639005]))
