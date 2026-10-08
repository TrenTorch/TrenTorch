"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/12-glow/01-actnorm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-glow-actnorm")
actnorm_forward = _module.actnorm_forward


import numpy as np


def test_1_identity_scale_and_zero_bias_keep_the_input():
    x = np.array([[1.0, 2.0]])
    np.testing.assert_allclose(actnorm_forward(x, np.ones(2), np.zeros(2)), x)


def test_2_hand_value():
    np.testing.assert_allclose(actnorm_forward(np.array([1.0]), np.array([2.0]), np.array([3.0])), [8.0])


def test_3_bias_is_added_before_scaling():
    np.testing.assert_allclose(actnorm_forward(np.array([0.0]), np.array([4.0]), np.array([1.0])), [4.0])


def test_4_keeps_the_shape():
    assert actnorm_forward(np.ones((2, 3, 4)), np.ones(4), np.zeros(4)).shape == (2, 3, 4)


def test_5_scales_each_channel_separately():
    out = actnorm_forward(np.array([[1.0, 1.0]]), np.array([2.0, 3.0]), np.zeros(2))
    np.testing.assert_allclose(out, [[2.0, 3.0]])


def test_6_does_not_mutate_input():
    x = np.array([1.0])
    actnorm_forward(x, np.ones(1), np.zeros(1))
    np.testing.assert_array_equal(x, [1.0])

