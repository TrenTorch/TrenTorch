"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/05-highway-networks/01-highway-gate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-highway-gate")
highway_gate = _module.highway_gate


import numpy as np


def test_1_output_shape_matches_batch_and_features():
    t = highway_gate(np.ones((3, 2)), np.eye(2), np.zeros(2))
    assert t.shape == (3, 2)


def test_2_gate_values_are_strictly_between_zero_and_one():
    rng = np.random.default_rng(0)
    t = highway_gate(rng.normal(size=(10, 4)) * 5, rng.normal(size=(4, 4)), np.zeros(4))
    assert np.all(t > 0) and np.all(t < 1)


def test_3_zero_pre_activation_gives_one_half():
    t = highway_gate(np.zeros((1, 3)), np.eye(3), np.zeros(3))
    np.testing.assert_allclose(t, 0.5)


def test_4_large_positive_bias_opens_the_gate():
    t = highway_gate(np.zeros((1, 2)), np.eye(2), np.array([50.0, 50.0]))
    np.testing.assert_allclose(t, 1.0, atol=1e-6)


def test_5_large_negative_bias_closes_the_gate():
    t = highway_gate(np.zeros((1, 2)), np.eye(2), np.array([-50.0, -50.0]))
    np.testing.assert_allclose(t, 0.0, atol=1e-6)


def test_6_matches_a_hand_computed_gate():
    # z = 1*1 + 0 + b = 0 with b=-1 -> sigmoid(0) = 0.5 only if z=0; here z=1-1=0
    t = highway_gate(np.array([[1.0]]), np.array([[1.0]]), np.array([-1.0]))
    np.testing.assert_allclose(t, [[0.5]])

