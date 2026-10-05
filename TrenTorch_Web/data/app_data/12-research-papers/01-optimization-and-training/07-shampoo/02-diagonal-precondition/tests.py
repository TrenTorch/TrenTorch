"""
pytest data/app_data/12-research-papers/01-optimization-and-training/07-shampoo/02-diagonal-precondition/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-shampoo-diagonal-precondition")
precondition_diag = _module.precondition_diag


import numpy as np


def test_1_hand_case():
    out = precondition_diag(np.array([16.0, 1.0]), np.ones((2, 2)), np.array([1.0, 16.0]))
    np.testing.assert_allclose(out, [[0.5, 0.25], [1.0, 0.5]])


def test_2_unit_preconditioners_leave_gradient_unchanged():
    G = np.array([[2.0, -1.0]])
    np.testing.assert_allclose(precondition_diag(np.ones(1), G, np.ones(2)), G)


def test_3_keeps_the_shape():
    assert precondition_diag(np.ones(3), np.ones((3, 4)), np.ones(4)).shape == (3, 4)


def test_4_scales_by_fourth_root_of_eigenvalue():
    out = precondition_diag(np.array([81.0]), np.array([[1.0]]), np.array([1.0]))
    assert abs(out[0, 0] - 1.0 / 3.0) < 1e-12


def test_5_is_linear_in_the_gradient():
    L, R = np.array([4.0, 9.0]), np.array([1.0, 16.0])
    G = np.array([[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(precondition_diag(L, 2 * G, R), 2 * precondition_diag(L, G, R))


def test_6_does_not_mutate_gradient():
    G = np.ones((1, 1))
    precondition_diag(np.array([1.0]), G, np.array([1.0]))
    np.testing.assert_array_equal(G, np.ones((1, 1)))

