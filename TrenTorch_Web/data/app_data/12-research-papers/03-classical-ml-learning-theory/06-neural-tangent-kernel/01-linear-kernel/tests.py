"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/06-neural-tangent-kernel/01-linear-kernel/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ntk-linear-kernel")
linear_kernel_matrix = _module.linear_kernel_matrix


import numpy as np


def test_1_output_shape():
    assert linear_kernel_matrix(np.ones((3, 2)), np.ones((4, 2))).shape == (3, 4)


def test_2_matches_a_hand_value():
    K = linear_kernel_matrix(np.array([[1.0, 2.0]]), np.array([[3.0, 4.0]]))
    np.testing.assert_allclose(K, [[11.0]])


def test_3_square_kernel_is_symmetric():
    X = np.array([[1.0, 0.0], [2.0, 3.0]])
    K = linear_kernel_matrix(X, X)
    np.testing.assert_allclose(K, K.T)


def test_4_square_kernel_is_positive_semidefinite():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(5, 3))
    eigs = np.linalg.eigvalsh(linear_kernel_matrix(X, X))
    assert eigs.min() > -1e-9


def test_5_orthogonal_inputs_have_zero_kernel():
    K = linear_kernel_matrix(np.array([[1.0, 0.0]]), np.array([[0.0, 1.0]]))
    np.testing.assert_allclose(K, [[0.0]])


def test_6_does_not_mutate_inputs():
    X = np.ones((2, 2))
    linear_kernel_matrix(X, X)
    np.testing.assert_array_equal(X, np.ones((2, 2)))

