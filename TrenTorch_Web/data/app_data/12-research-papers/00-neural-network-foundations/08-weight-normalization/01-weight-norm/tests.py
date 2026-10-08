"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/08-weight-normalization/01-weight-norm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-weight-norm")
weight_norm = _module.weight_norm


import numpy as np


def test_1_each_row_has_norm_equal_to_g():
    W = weight_norm(np.array([[3.0, 4.0], [1.0, 0.0]]), np.array([2.0, 5.0]))
    np.testing.assert_allclose(np.linalg.norm(W, axis=1), [2.0, 5.0])


def test_2_output_shape_matches_v():
    assert weight_norm(np.ones((3, 4)), np.ones(3)).shape == (3, 4)


def test_3_direction_is_unchanged_by_scaling_v():
    a = weight_norm(np.array([[1.0, 2.0]]), np.array([1.0]))
    b = weight_norm(np.array([[10.0, 20.0]]), np.array([1.0]))
    np.testing.assert_allclose(a, b)


def test_4_unit_g_gives_unit_norm_rows():
    W = weight_norm(np.array([[2.0, 2.0, 1.0]]), np.array([1.0]))
    np.testing.assert_allclose(np.linalg.norm(W, axis=1), [1.0])


def test_5_matches_a_hand_computed_row():
    # v = [3, 4], norm 5, g = 10 -> [6, 8]
    W = weight_norm(np.array([[3.0, 4.0]]), np.array([10.0]))
    np.testing.assert_allclose(W, [[6.0, 8.0]])


def test_6_does_not_mutate_inputs():
    v = np.array([[3.0, 4.0]])
    weight_norm(v, np.array([1.0]))
    np.testing.assert_array_equal(v, [[3.0, 4.0]])

