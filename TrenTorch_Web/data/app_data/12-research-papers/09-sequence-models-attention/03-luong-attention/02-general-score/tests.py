"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/03-luong-attention/02-general-score/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-luong-general-score")
general_score = _module.general_score


import numpy as np


def test_1_identity_matrix_gives_the_dot_product():
    assert abs(general_score(np.array([1.0, 2.0]), np.eye(2), np.array([3.0, 4.0])) - 11.0) < 1e-12


def test_2_zero_matrix_gives_zero():
    assert general_score(np.ones(2), np.zeros((2, 2)), np.ones(2)) == 0.0


def test_3_hand_value_with_rectangular_matrix():
    assert abs(general_score(np.array([1.0]), np.array([[2.0, 3.0]]), np.array([1.0, 1.0])) - 5.0) < 1e-12


def test_4_is_linear_in_the_decoder_state():
    W = np.array([[1.0, 2.0]])
    s = np.array([1.0, 1.0])
    assert abs(general_score(np.array([2.0]), W, s) - 2 * general_score(np.array([1.0]), W, s)) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(general_score(np.ones(1), np.ones((1, 1)), np.ones(1)), float)


def test_6_does_not_mutate_inputs():
    W = np.eye(2)
    general_score(np.ones(2), W, np.ones(2))
    np.testing.assert_array_equal(W, np.eye(2))

