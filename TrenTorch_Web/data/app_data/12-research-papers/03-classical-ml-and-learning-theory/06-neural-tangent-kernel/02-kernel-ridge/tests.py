"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/06-neural-tangent-kernel/02-kernel-ridge/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ntk-kernel-ridge")
kernel_ridge_predict = _module.kernel_ridge_predict


import numpy as np


def test_1_identity_kernel_with_ridge_one_halves_targets():
    y = np.array([2.0, 4.0])
    out = kernel_ridge_predict(np.eye(2), y, np.eye(2), 1.0)
    np.testing.assert_allclose(out, [1.0, 2.0])


def test_2_zero_ridge_interpolates_the_training_targets():
    K = np.array([[2.0, 0.0], [0.0, 3.0]])
    y = np.array([4.0, 9.0])
    np.testing.assert_allclose(kernel_ridge_predict(K, y, K, 0.0), y)


def test_3_output_has_one_prediction_per_test_point():
    assert kernel_ridge_predict(np.eye(3), np.ones(3), np.ones((5, 3)), 1.0).shape == (5,)


def test_4_larger_ridge_shrinks_predictions():
    K = np.eye(2)
    y = np.array([1.0, 1.0])
    small = np.abs(kernel_ridge_predict(K, y, K, 0.1)).sum()
    large = np.abs(kernel_ridge_predict(K, y, K, 10.0)).sum()
    assert large < small


def test_5_does_not_mutate_the_targets():
    y = np.array([1.0, 2.0])
    kernel_ridge_predict(np.eye(2), y, np.eye(2), 1.0)
    np.testing.assert_array_equal(y, [1.0, 2.0])


def test_6_matches_a_hand_computed_scalar_case():
    # K = [[2]], y = [6], lam = 1 -> alpha = 6 / 3 = 2 -> prediction = K_test * 2
    out = kernel_ridge_predict(np.array([[2.0]]), np.array([6.0]), np.array([[1.0]]), 1.0)
    np.testing.assert_allclose(out, [2.0])

