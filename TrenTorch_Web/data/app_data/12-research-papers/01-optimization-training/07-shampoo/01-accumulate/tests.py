"""
pytest data/app_data/12-research-papers/01-optimization-and-training/07-shampoo/01-accumulate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-shampoo-accumulate")
accumulate_preconditioners = _module.accumulate_preconditioners


import numpy as np


def test_1_hand_case_single_row():
    L, R = accumulate_preconditioners(np.zeros((1, 1)), np.zeros((2, 2)), np.array([[1.0, 0.0]]))
    np.testing.assert_allclose(L, [[1.0]])
    np.testing.assert_allclose(R, [[1.0, 0.0], [0.0, 0.0]])


def test_2_accumulates_across_calls():
    L, R = np.zeros((1, 1)), np.zeros((1, 1))
    L, R = accumulate_preconditioners(L, R, np.array([[2.0]]))
    L, R = accumulate_preconditioners(L, R, np.array([[2.0]]))
    assert abs(L[0, 0] - 8.0) < 1e-12 and abs(R[0, 0] - 8.0) < 1e-12


def test_3_output_shapes_match_dimensions():
    L, R = accumulate_preconditioners(np.zeros((3, 3)), np.zeros((4, 4)), np.ones((3, 4)))
    assert L.shape == (3, 3) and R.shape == (4, 4)


def test_4_preconditioners_are_symmetric():
    rng = np.random.default_rng(0)
    G = rng.standard_normal((3, 4))
    L, R = accumulate_preconditioners(np.zeros((3, 3)), np.zeros((4, 4)), G)
    np.testing.assert_allclose(L, L.T, atol=1e-12)
    np.testing.assert_allclose(R, R.T, atol=1e-12)


def test_5_preconditioners_are_nonnegative_definite_diagonal():
    L, R = accumulate_preconditioners(np.zeros((2, 2)), np.zeros((2, 2)), np.eye(2))
    assert np.all(np.diag(L) >= 0) and np.all(np.diag(R) >= 0)


def test_6_does_not_mutate_inputs():
    L = np.zeros((1, 1))
    accumulate_preconditioners(L, np.zeros((1, 1)), np.array([[1.0]]))
    np.testing.assert_array_equal(L, np.zeros((1, 1)))

