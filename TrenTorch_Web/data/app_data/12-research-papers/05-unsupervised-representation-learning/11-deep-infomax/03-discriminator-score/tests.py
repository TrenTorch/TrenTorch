"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/11-deep-infomax/03-discriminator-score/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dim-discriminator-score")
discriminator_score = _module.discriminator_score


import numpy as np


def test_1_identity_gives_the_dot_product():
    assert abs(discriminator_score(np.array([1.0, 2.0]), np.array([3.0, 4.0]), np.eye(2)) - 11.0) < 1e-12


def test_2_zero_matrix_gives_zero():
    assert discriminator_score(np.ones(3), np.ones(2), np.zeros((3, 2))) == 0.0


def test_3_hand_value():
    assert abs(discriminator_score(np.array([1.0]), np.array([2.0]), np.array([[3.0]])) - 6.0) < 1e-12


def test_4_linear_in_the_local_vector():
    W = np.array([[1.0], [1.0]])
    g = np.array([1.0])
    a = discriminator_score(np.array([1.0, 0.0]), g, W)
    b = discriminator_score(np.array([2.0, 0.0]), g, W)
    assert abs(b - 2 * a) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(discriminator_score(np.ones(1), np.ones(1), np.ones((1, 1))), float)


def test_6_does_not_mutate_inputs():
    g = np.array([2.0])
    discriminator_score(np.ones(1), g, np.ones((1, 1)))
    np.testing.assert_array_equal(g, [2.0])

