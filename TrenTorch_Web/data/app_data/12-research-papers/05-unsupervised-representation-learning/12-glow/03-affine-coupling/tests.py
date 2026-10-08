"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/12-glow/03-affine-coupling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-glow-affine-coupling")
affine_coupling_forward = _module.affine_coupling_forward


import numpy as np


def test_1_zero_scale_and_shift_is_identity():
    xa = np.array([1.0])
    xb = np.array([2.0])
    ya, yb = affine_coupling_forward(xa, xb, np.zeros(1), np.zeros(1))
    np.testing.assert_allclose(ya, xa)
    np.testing.assert_allclose(yb, xb)


def test_2_first_half_is_unchanged():
    ya, _ = affine_coupling_forward(np.array([3.0, 4.0]), np.array([1.0, 1.0]), np.ones(2), np.ones(2))
    np.testing.assert_allclose(ya, [3.0, 4.0])


def test_3_log_scale_of_log_two_doubles_the_second_half():
    _, yb = affine_coupling_forward(np.zeros(1), np.array([3.0]), np.array([np.log(2.0)]), np.zeros(1))
    np.testing.assert_allclose(yb, [6.0])


def test_4_shift_is_added_after_scaling():
    _, yb = affine_coupling_forward(np.zeros(1), np.array([1.0]), np.array([0.0]), np.array([5.0]))
    np.testing.assert_allclose(yb, [6.0])


def test_5_output_shapes_match_inputs():
    ya, yb = affine_coupling_forward(np.zeros((2, 3)), np.ones((2, 3)), np.zeros((2, 3)), np.zeros((2, 3)))
    assert ya.shape == (2, 3) and yb.shape == (2, 3)


def test_6_does_not_mutate_inputs():
    xb = np.array([2.0])
    affine_coupling_forward(np.zeros(1), xb, np.zeros(1), np.zeros(1))
    np.testing.assert_array_equal(xb, [2.0])

