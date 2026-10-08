"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/09-cpc/02-bilinear-score/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-cpc-bilinear-score")
bilinear_score = _module.bilinear_score


import numpy as np


def test_1_identity_matrix_gives_the_dot_product():
    assert abs(bilinear_score(np.array([1.0, 2.0]), np.eye(2), np.array([3.0, 4.0])) - 11.0) < 1e-12


def test_2_zero_matrix_gives_zero():
    assert bilinear_score(np.ones(2), np.zeros((2, 2)), np.ones(2)) == 0.0


def test_3_hand_value_with_rectangular_matrix():
    W = np.array([[1.0, 0.0, 2.0]])
    # c W = [3, 0, 6], dot z = 3 + 0 + 6 = 9
    assert abs(bilinear_score(np.array([3.0]), W, np.array([1.0, 5.0, 1.0])) - 9.0) < 1e-12


def test_4_is_linear_in_the_context():
    W = np.array([[1.0, 2.0], [0.0, 1.0]])
    z = np.array([1.0, 1.0])
    a = bilinear_score(np.array([1.0, 0.0]), W, z)
    b = bilinear_score(np.array([2.0, 0.0]), W, z)
    assert abs(b - 2 * a) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(bilinear_score(np.ones(1), np.ones((1, 1)), np.ones(1)), float)


def test_6_does_not_mutate_inputs():
    c = np.array([1.0])
    bilinear_score(c, np.ones((1, 1)), np.ones(1))
    np.testing.assert_array_equal(c, [1.0])

