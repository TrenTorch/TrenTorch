"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/08-weight-normalization/03-weight-norm-linear/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-weight-norm-linear")
weight_norm_linear = _module.weight_norm_linear


import numpy as np


def test_1_output_shape_is_batch_by_out():
    out = weight_norm_linear(np.ones((4, 3)), np.ones((2, 3)), np.ones(2), np.zeros(2))
    assert out.shape == (4, 2)


def test_2_bias_is_added():
    out = weight_norm_linear(np.zeros((1, 2)), np.eye(2), np.ones(2), np.array([1.0, -1.0]))
    np.testing.assert_allclose(out, [[1.0, -1.0]])


def test_3_identity_direction_and_unit_scale_is_identity_map():
    x = np.array([[2.0, 3.0]])
    out = weight_norm_linear(x, np.eye(2), np.ones(2), np.zeros(2))
    np.testing.assert_allclose(out, x)


def test_4_scale_g_multiplies_the_output():
    x = np.array([[1.0, 0.0]])
    out = weight_norm_linear(x, np.eye(2), np.array([5.0, 1.0]), np.zeros(2))
    np.testing.assert_allclose(out, [[5.0, 0.0]])


def test_5_scaling_v_does_not_change_the_output():
    x = np.array([[1.0, 2.0]])
    a = weight_norm_linear(x, np.array([[1.0, 1.0]]), np.array([1.0]), np.zeros(1))
    b = weight_norm_linear(x, np.array([[7.0, 7.0]]), np.array([1.0]), np.zeros(1))
    np.testing.assert_allclose(a, b)


def test_6_does_not_mutate_inputs():
    x = np.array([[1.0, 2.0]])
    weight_norm_linear(x, np.eye(2), np.ones(2), np.zeros(2))
    np.testing.assert_array_equal(x, [[1.0, 2.0]])

