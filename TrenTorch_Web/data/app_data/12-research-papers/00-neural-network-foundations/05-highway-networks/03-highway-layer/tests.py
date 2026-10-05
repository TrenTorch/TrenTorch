"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/05-highway-networks/03-highway-layer/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-highway-layer")
highway_layer = _module.highway_layer


import numpy as np


def test_1_output_shape_matches_input():
    x = np.ones((3, 4))
    out = highway_layer(x, np.eye(4), np.zeros(4), np.eye(4), np.zeros(4))
    assert out.shape == (3, 4)


def test_2_very_negative_gate_bias_returns_the_input():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(2, 3))
    out = highway_layer(x, rng.normal(size=(3, 3)), np.zeros(3), np.eye(3), np.full(3, -60.0))
    np.testing.assert_allclose(out, x, atol=1e-6)


def test_3_very_positive_gate_bias_returns_the_transform():
    x = np.array([[0.5, -0.5]])
    W_h = np.eye(2)
    out = highway_layer(x, W_h, np.zeros(2), np.eye(2), np.full(2, 60.0))
    np.testing.assert_allclose(out, np.tanh(x), atol=1e-6)


def test_4_zero_input_and_zero_biases_give_zero():
    out = highway_layer(np.zeros((1, 2)), np.eye(2), np.zeros(2), np.eye(2), np.zeros(2))
    np.testing.assert_allclose(out, 0.0)


def test_5_output_is_bounded_between_input_and_transform():
    x = np.array([[1.0]])
    out = highway_layer(x, np.array([[0.0]]), np.zeros(1), np.array([[0.0]]), np.zeros(1))
    np.testing.assert_allclose(out, [[0.5]])


def test_6_does_not_mutate_the_input():
    x = np.array([[1.0, 2.0]])
    highway_layer(x, np.eye(2), np.zeros(2), np.eye(2), np.zeros(2))
    np.testing.assert_array_equal(x, [[1.0, 2.0]])

