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
    _close(solve([1000.0, 1001.0]), np.array([0.2689414213699951, 0.7310585786300049]))


def test_02_readme_example_2():
    _close(solve([0.0, 0.0, 0.0]), np.array([0.3333333333333333, 0.3333333333333333, 0.3333333333333333]))


def test_03_readme_example_3():
    _close(solve([-1000.0, 0.0]), np.array([0.0, 1.0]))


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve(np.array([]))


def test_05_random_valid_case_1():
    _close(solve([3.8, 4.89, 3.38, 0.04, 2.02, 2.95]), np.array([0.1904523308994644, 0.5664574298534784, 0.12513609834385797, 0.0044344426264571035, 0.03211752822587116, 0.08140217005087097]))


def test_06_random_valid_case_2():
    _close(solve([1.81, 4.86, 0.35, 2.26, 4.46, 3.54]), np.array([0.022877753523829095, 0.48307164526964363, 0.00531304425255968, 0.035879459628061806, 0.32381260749565943, 0.12904548983024636]))


def test_07_random_valid_case_3():
    _close(solve([2.8, -4.61, 3.77, -4.49, 4.3, 2.89]), np.array([0.10851759706512033, 6.567166958517392e-05, 0.28626339392036065, 7.404460069524471e-05, 0.4863421287060999, 0.11873716403813872]))


def test_08_random_valid_case_4():
    _close(solve([1.75, -4.75, 0.04, 2.48, 4.48, 3.74]), np.array([0.03860128905153698, 5.803469085953677e-05, 0.006981652740348874, 0.08010078634206781, 0.5918692038499974, 0.2823890333251895]))


def test_09_random_valid_case_5():
    _close(solve([-2.9, -1.23, -4.7, 4.17, 3.69, 0.85]), np.array([0.0005120517910427844, 0.002720105034866419, 8.464159177124433e-05, 0.6022487074687394, 0.3726614979183709, 0.021772996195209258]))


def test_10_random_valid_case_6():
    _close(solve([4.98, -3.54, -0.32, 4.81, 3.2, -3.41]), np.array([0.4956086288980551, 9.884390015292891e-05, 0.0024738770122196565, 0.4181275630028625, 0.0835785209476969, 0.00011256623901266026]))


def test_11_random_valid_case_7():
    _close(solve([2.21, 1.7, -3.93, -4.15, -3.23, 1.35]), np.array([0.49215470101110237, 0.2955367220488396, 0.0010605557890650248, 0.0008511159570126117, 0.0021356970916531835, 0.2082612081023272]))


def test_12_random_valid_case_8():
    _close(solve([3.88, 3.53, 1.45, 0.89, -2.51, -3.42]), np.array([0.5418978763817279, 0.3818689793300673, 0.04770697261976142, 0.027250655169194962, 0.0009094434715572989, 0.0003660730276910578]))
