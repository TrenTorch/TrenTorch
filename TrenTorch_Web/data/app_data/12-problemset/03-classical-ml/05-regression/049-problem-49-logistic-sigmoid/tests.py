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
    _close(solve([0.0]), np.array([0.5]))


def test_02_readme_example_2():
    _close(solve([2.0, -2.0]), np.array([0.8807970779778823, 0.11920292202211755]))


def test_03_readme_example_3():
    _close(solve([1000.0, -1000.0]), np.array([1.0, 0.0]))


def test_04_random_valid_case_1():
    _close(solve([4.13, 3.52, -2.73, 1.66, 4.79, 4.3]), np.array([0.9841716860329102, 0.97125150407346, 0.061226162819908, 0.8402380030563309, 0.9917560699353984, 0.9866130821723351]))


def test_05_random_valid_case_2():
    _close(solve([-0.67, -0.39, 0.4, 2.2, -3.08, 1.22]), np.array([0.33849684079704756, 0.40371730070321216, 0.598687660112452, 0.9002495108803148, 0.04393981539614133, 0.7720635494267837]))


def test_06_random_valid_case_3():
    _close(solve([4.05, 0.74, 3.65, 2.48, -1.97, 1.99]), np.array([0.9828759666842724, 0.676995856238523, 0.9746672967731284, 0.9227277978633401, 0.12238888682304888, 0.8797431375322491]))


def test_07_random_valid_case_4():
    _close(solve([0.26, 3.34, 0.59, 4.19, -1.21, 1.89]), np.array([0.5646362918030292, 0.965775842307604, 0.6433651456944017, 0.9850797022077058, 0.22970105095339816, 0.8687555305614766]))


def test_08_random_valid_case_5():
    _close(solve([0.35, 4.13, -3.0, -3.86, -0.41, 3.02]), np.array([0.5866175789173301, 0.9841716860329102, 0.04742587317756679, 0.020633297226906204, 0.3989121211516303, 0.9534695254852685]))


def test_09_random_valid_case_6():
    _close(solve([3.17, -3.24, -0.69, -2.57, 2.59, 4.46]), np.array([0.9596895845772907, 0.037687890508605916, 0.33403307324817977, 0.07109430408428717, 0.9302152171234199, 0.9885697968735292]))


def test_10_random_valid_case_7():
    _close(solve([-2.42, -0.84, 1.59, -1.39, 2.03, -4.24]), np.array([0.08166025546159467, 0.30153478399746125, 0.8306161030659813, 0.1994077568486685, 0.8839110779310051, 0.014202961372691125]))


def test_11_random_valid_case_8():
    _close(solve([-2.97, 2.92, 1.14, -3.46, -0.26, -4.75]), np.array([0.048799722998799984, 0.9488262990829084, 0.7576796390037048, 0.03047203326464416, 0.43536370819697084, 0.008577485413711986]))


def test_12_random_valid_case_9():
    _close(solve([2.32, -3.14, -1.68, -1.58, -0.51, 1.74]), np.array([0.9105199406664386, 0.041487119301695845, 0.15709546888545275, 0.17079548202237446, 0.3751935255315707, 0.8506870654691563]))
