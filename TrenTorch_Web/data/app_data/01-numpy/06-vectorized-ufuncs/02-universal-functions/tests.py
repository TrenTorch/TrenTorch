"""
pytest data/app_data/01-numpy/06-vectorized-ufuncs/02-universal-functions/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/06-vectorized-ufuncs/{Path(__file__).resolve().parent.name}")
sqrt_all = _module.sqrt_all
exponentiate = _module.exponentiate
natural_log = _module.natural_log
absolute_values = _module.absolute_values


def test_sqrt_all_correctness():
    arr = np.array([1.0, 4.0, 9.0, 16.0])
    np.testing.assert_allclose(sqrt_all(arr), [1.0, 2.0, 3.0, 4.0])


def test_exponentiate_and_natural_log_are_inverses():
    arr = np.array([0.5, 1.0, 2.0])
    result = natural_log(exponentiate(arr))
    np.testing.assert_allclose(result, arr, atol=1e-10)


def test_absolute_values_correctness_with_negative_and_positive_inputs():
    arr = np.array([-3, 2, -1, 0])
    np.testing.assert_array_equal(absolute_values(arr), [3, 2, 1, 0])


def test_all_functions_preserve_shape():
    arr = np.array([[1.0, 4.0], [9.0, 16.0]])
    assert sqrt_all(arr).shape == (2, 2)
    assert exponentiate(arr).shape == (2, 2)
    assert natural_log(arr).shape == (2, 2)
    assert absolute_values(arr).shape == (2, 2)
