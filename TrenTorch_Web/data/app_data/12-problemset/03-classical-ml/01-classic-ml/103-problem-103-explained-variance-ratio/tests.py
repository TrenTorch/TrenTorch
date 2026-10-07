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
    _close(solve([2.0, 1.0]), np.array([0.6666666666666666, 0.3333333333333333]))


def test_02_readme_example_2():
    _close(solve([5.0, 3.0, 2.0]), np.array([0.5, 0.3, 0.2]))


def test_03_readme_example_3():
    _close(solve([0.0, 0.0]), np.array([0.0, 0.0]))


def test_04_random_valid_case_1():
    _close(solve([0.0, 0.0]), np.array([0.0, 0.0]))


def test_05_random_valid_case_2():
    _close(solve([10.368051435300561, 8.76221259135632, 6.059985374693656, 5.340957265316125]), np.array([0.3395886559118603, 0.28699201728317936, 0.19848496133334365, 0.17493436547161667]))


def test_06_random_valid_case_3():
    _close(solve([16.31817316339087, 10.054533472279678, 6.7057843928553, 3.7247184952836894]), np.array([0.4433899481737853, 0.27319719128775927, 0.18220651078045375, 0.10120634975800176]))


def test_07_random_valid_case_4():
    _close(solve([13.06727059210834, 9.51596263386786, 7.455860955879063, 3.4159743895733077]), np.array([0.3905916547206871, 0.2844400875625381, 0.22286192419424738, 0.10210633352252732]))


def test_08_random_valid_case_5():
    _close(solve([12.95595131216969, 6.316404176515753, 4.8271197117419264, 2.296671466239303]), np.array([0.49082737248655317, 0.23929266101904842, 0.1828721355696081, 0.08700783092479039]))


def test_09_random_valid_case_6():
    _close(solve([14.126671871481788, 7.543464628958787, 4.421659826050002, 1.980951292557028]), np.array([0.5032165737099676, 0.2687113043341892, 0.1575071982996729, 0.07056492365617019]))


def test_10_random_valid_case_7():
    _close(solve([13.983153681731988, 8.893833577847365, 5.799437841838559, 4.858260612867788]), np.array([0.4169758381178207, 0.26521296944967676, 0.17293848796584999, 0.14487270446665257]))


def test_11_random_valid_case_8():
    _close(solve([15.114608069187181, 9.631245661343808, 7.694800696322586, 3.253545573146439]), np.array([0.4234471726271264, 0.26982662901378385, 0.21557565924779326, 0.09115053911129645]))


def test_12_random_valid_case_9():
    _close(solve([14.533425853364417, 9.028537428298977, 7.357461783144414, 4.828004459001706]), np.array([0.40655862664711184, 0.2525646612516722, 0.20581792540479, 0.13505878669642588]))
