"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/09-scikit-learn/03-standard-scale/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sklearn-standard-scale")
standard_scale = _module.standard_scale


import numpy as np


def test_1_columns_have_zero_mean():
    out = standard_scale(np.array([[1.0, 10.0], [3.0, 30.0], [5.0, 50.0]]))
    np.testing.assert_allclose(out.mean(axis=0), 0.0, atol=1e-12)


def test_2_columns_have_unit_standard_deviation():
    out = standard_scale(np.array([[1.0, 10.0], [3.0, 30.0], [5.0, 50.0]]))
    np.testing.assert_allclose(out.std(axis=0), 1.0, atol=1e-12)


def test_3_matches_a_hand_value():
    np.testing.assert_allclose(standard_scale(np.array([[1.0], [3.0]])), [[-1.0], [1.0]])


def test_4_constant_column_becomes_zeros():
    np.testing.assert_allclose(standard_scale(np.array([[2.0], [2.0]])), [[0.0], [0.0]])


def test_5_keeps_the_shape():
    assert standard_scale(np.ones((4, 3)) * np.arange(3)).shape == (4, 3)


def test_6_does_not_mutate_the_input():
    X = np.array([[1.0], [3.0]])
    standard_scale(X)
    np.testing.assert_array_equal(X, [[1.0], [3.0]])

