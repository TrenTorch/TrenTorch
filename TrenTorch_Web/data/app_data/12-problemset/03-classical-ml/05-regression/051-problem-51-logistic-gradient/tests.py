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
    _close(solve([[1.0, 2.0], [3.0, 4.0]], [1, 0], [0.0, 0.0]), (np.array([0.5, 0.5]), 0.0))


def test_02_readme_example_2():
    _close(solve([[1.0], [2.0], [3.0]], [0, 1, 1], [0.5]), (np.array([-0.1542333609857349]), 0.05703079534183438))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([[1.0, 2.0]], [0], [0.2])


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([[1.0, 2.0], [2.0, 1.0]], [], [0.2, 0.7])


def test_05_random_valid_case_1():
    _close(solve([[2.62, 4.51, 1.98], [3.77, -0.08, 4.07], [3.4, 4.11, 1.9], [-0.1, 3.45, -1.39], [-3.6, 4.34, -1.69], [-3.2, 4.44, -4.69], [-3.76, -0.8, 3.8], [0.5, -1.46, 4.07]], [0, 1, 1, 0, 0, 1, 1, 0], [-3.17, 0.22, -0.16]), (np.array([-1.3513860867701215, 0.36468673229283927, -1.0572684618656754]), -0.01775019910939135))


def test_06_random_valid_case_2():
    _close(solve([[2.9, -1.28, 4.19], [2.72, -2.03, 3.26], [1.93, 0.28, -4.5], [-4.68, 1.7, -1.05], [-1.57, -1.75, 1.07], [0.69, 3.97, 3.83], [4.5, -0.61, 1.58], [0.77, -2.06, -3.13]], [1, 1, 0, 0, 1, 0, 0, 0], [0.34, -4.47, 2.39]), (np.array([0.6470141971790395, -0.30260987154758195, -0.1466371429965518]), 0.2349432680489005))


def test_07_random_valid_case_3():
    _close(solve([[-3.83, 2.62, -0.21], [0.91, 3.53, 4.53], [1.91, 4.89, 2.52], [1.99, -4.24, 2.39], [1.9, -3.5, 2.31], [-4.57, 0.29, -3.48], [-1.48, 4.96, -2.45], [0.64, 0.39, -0.23]], [0, 0, 1, 1, 0, 0, 0, 0], [3.38, 2.18, -1.2]), (np.array([-0.23835749399182482, 1.6258940957830164, -0.06250900534394938]), 0.24787086971666844))


def test_08_random_valid_case_4():
    _close(solve([[-3.83, -1.09, 2.29], [3.33, -3.33, -4.63], [4.26, 4.81, 4.66], [-1.16, 2.39, -1.51], [3.18, 2.59, -4.02], [3.91, 2.52, 2.36], [2.07, -4.4, 2.8], [2.12, -4.78, -3.15]], [0, 0, 1, 0, 1, 0, 0, 0], [0.56, 3.61, 2.73]), (np.array([-0.09620862021488455, 0.3838637874449356, 0.4975371077356658]), 0.2577457928050207))


def test_09_random_valid_case_5():
    _close(solve([[2.59, -1.06, 3.0], [-3.49, 3.39, 2.54], [-4.19, -0.68, 2.83], [-2.4, -2.91, 3.07], [3.0, -4.17, -1.16], [-4.92, -3.75, 3.24], [-2.34, -1.86, -2.64], [1.22, 3.0, 3.27]], [0, 0, 1, 1, 1, 1, 0, 0], [3.42, -2.3, 3.9]), (np.array([0.928235617570735, 0.32019777858970294, 0.4785655438401145]), 0.1423752418481561))


def test_10_random_valid_case_6():
    _close(solve([[-0.62, -0.29, 2.49], [-0.59, -0.27, 0.89], [-4.27, 3.42, 0.26], [3.46, 4.96, 2.97], [0.7, -1.63, 3.65], [2.27, -2.27, 2.22], [2.82, -3.6, 4.87], [4.03, -0.37, -2.09]], [1, 1, 1, 1, 1, 0, 0, 1], [2.15, 3.35, 3.87]), (np.array([0.33847921484854737, -0.7104614643039461, 1.0321264193527708]), 0.13515966323534986))


def test_11_random_valid_case_7():
    _close(solve([[-2.3, 4.43, -0.97], [4.82, 4.66, 0.79], [-0.87, -3.84, 2.62], [-3.59, 3.71, -1.8], [2.78, -1.42, 4.39], [-0.22, 2.94, 3.98], [-3.66, -2.33, 3.34], [-4.35, 1.4, 0.09]], [1, 0, 0, 0, 0, 1, 1, 1], [-0.34, 1.46, 3.48]), (np.array([0.5949968520109149, 0.19492561051401672, 0.8367891889334897]), 0.44107303878809184))


def test_12_random_valid_case_8():
    _close(solve([[0.95, 3.09, 4.13], [-2.44, 1.52, 0.13], [-0.74, -3.1, -0.09], [2.66, 1.84, -0.26], [1.06, 0.68, -0.17], [-3.26, 4.7, 0.64], [-2.61, 1.89, -3.19], [-3.09, -3.27, 2.08]], [0, 0, 1, 0, 0, 0, 0, 0], [0.78, 2.98, 2.19]), (np.array([-0.04188444979302859, 1.857152716941421, 0.5579545918531269]), 0.4879280573298541))
