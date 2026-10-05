"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/03-negative-sampling/01-ns-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ns-loss")
negative_sampling_loss = _module.negative_sampling_loss


import numpy as np


def test_1_zero_vectors_give_k_plus_one_times_log_two():
    loss = negative_sampling_loss(np.zeros(2), np.zeros(2), np.zeros((3, 2)))
    assert abs(loss - 4 * np.log(2.0)) < 1e-9


def test_2_correct_pair_and_far_negatives_give_small_loss():
    v = np.array([1.0, 0.0])
    loss = negative_sampling_loss(v, np.array([20.0, 0.0]), np.array([[-20.0, 0.0]]))
    assert loss < 1e-6


def test_3_positive_pair_with_negative_score_is_penalized():
    v = np.array([1.0])
    assert negative_sampling_loss(v, np.array([-5.0]), np.zeros((1, 1))) > 4.0


def test_4_returns_a_python_float():
    assert isinstance(negative_sampling_loss(np.ones(2), np.ones(2), np.ones((2, 2))), float)


def test_5_more_negatives_add_more_loss():
    v = np.array([1.0])
    a = negative_sampling_loss(v, np.array([0.0]), np.zeros((1, 1)))
    b = negative_sampling_loss(v, np.array([0.0]), np.zeros((4, 1)))
    assert b > a


def test_6_does_not_mutate_inputs():
    v = np.array([1.0])
    negative_sampling_loss(v, np.array([1.0]), np.ones((1, 1)))
    np.testing.assert_array_equal(v, [1.0])

