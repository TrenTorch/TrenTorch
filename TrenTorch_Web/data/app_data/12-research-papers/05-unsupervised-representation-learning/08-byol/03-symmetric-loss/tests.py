"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/08-byol/03-symmetric-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-byol-symmetric-loss")
symmetric_byol_loss = _module.symmetric_byol_loss


import numpy as np


def test_1_identical_pairs_give_zero():
    v = np.array([1.0, 2.0])
    assert abs(symmetric_byol_loss(v, v, v, v)) < 1e-12


def test_2_orthogonal_pairs_give_four():
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert abs(symmetric_byol_loss(a, b, a, b) - 4.0) < 1e-12


def test_3_symmetric_in_swapping_the_two_directions():
    p1, z2, p2, z1 = np.array([1.0, 0.0]), np.array([1.0, 1.0]), np.array([0.0, 1.0]), np.array([1.0, 0.0])
    assert abs(symmetric_byol_loss(p1, z2, p2, z1) - symmetric_byol_loss(p2, z1, p1, z2)) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(symmetric_byol_loss(np.ones(2), np.ones(2), np.ones(2), np.ones(2)), float)


def test_5_equals_the_sum_of_two_single_losses():
    p1 = np.array([1.0, 0.0])
    z2 = np.array([0.0, 1.0])
    p2 = np.array([1.0, 1.0])
    z1 = np.array([1.0, 0.0])
    single = 2 - 2 * (p1 @ z2) / (np.linalg.norm(p1) * np.linalg.norm(z2))
    single2 = 2 - 2 * (p2 @ z1) / (np.linalg.norm(p2) * np.linalg.norm(z1))
    assert abs(symmetric_byol_loss(p1, z2, p2, z1) - (single + single2)) < 1e-12


def test_6_does_not_mutate_inputs():
    p1 = np.array([1.0])
    symmetric_byol_loss(p1, np.array([1.0]), np.array([1.0]), np.array([1.0]))
    np.testing.assert_array_equal(p1, [1.0])

