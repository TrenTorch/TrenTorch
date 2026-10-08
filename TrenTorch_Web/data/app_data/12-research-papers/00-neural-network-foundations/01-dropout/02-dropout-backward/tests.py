"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/01-dropout/02-dropout-backward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dropout-backward")
dropout_backward = _module.dropout_backward


def test_1_gradient_is_gated_by_the_mask():
    out = dropout_backward(np.array([1.0, 2.0]), np.array([1, 0]), p=0.5)
    np.testing.assert_allclose(out, [2.0, 0.0])


def test_2_dropped_units_receive_zero_gradient():
    out = dropout_backward(np.array([7.0, -3.0, 2.0]), np.array([0, 0, 0]), p=0.4)
    np.testing.assert_array_equal(out, [0.0, 0.0, 0.0])


def test_3_no_dropout_passes_gradient_through():
    g = np.array([[1.0, -1.0], [2.0, 0.5]])
    np.testing.assert_allclose(dropout_backward(g, np.ones_like(g), p=0.0), g)


def test_4_keeps_the_input_shape():
    out = dropout_backward(np.ones((2, 3)), np.ones((2, 3)), p=0.5)
    assert out.shape == (2, 3)


def test_5_does_not_mutate_the_gradient():
    g = np.array([1.0, 2.0])
    dropout_backward(g, np.array([1, 1]), p=0.5)
    np.testing.assert_array_equal(g, [1.0, 2.0])


def test_6_matches_the_forward_scaling_for_a_hand_case():
    out = dropout_backward(np.array([4.0, 8.0]), np.array([1, 1]), p=0.2)
    np.testing.assert_allclose(out, [5.0, 10.0])

