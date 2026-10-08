"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/10-vq-vae/03-vq-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vq-loss")
vq_loss = _module.vq_loss


import numpy as np


def test_1_matching_codes_give_zero():
    z = np.array([[1.0, 2.0]])
    assert abs(vq_loss(z, z, 0.25)) < 1e-12


def test_2_hand_value_with_zero_commitment_weight():
    # mean of squared differences: ((1-0)^2 + (2-0)^2) / 2 = 2.5
    assert abs(vq_loss(np.array([[1.0, 2.0]]), np.zeros((1, 2)), 0.0) - 2.5) < 1e-12


def test_3_commitment_weight_scales_the_loss():
    z = np.array([[1.0]])
    e = np.zeros((1, 1))
    assert abs(vq_loss(z, e, 1.0) - 2 * vq_loss(z, e, 0.0)) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(vq_loss(np.ones((2, 2)), np.zeros((2, 2)), 0.25), float)


def test_5_larger_mismatch_gives_larger_loss():
    e = np.zeros((1, 1))
    assert vq_loss(np.array([[3.0]]), e, 0.25) > vq_loss(np.array([[1.0]]), e, 0.25)


def test_6_does_not_mutate_inputs():
    z = np.array([[1.0]])
    vq_loss(z, np.zeros((1, 1)), 0.25)
    np.testing.assert_array_equal(z, [[1.0]])

