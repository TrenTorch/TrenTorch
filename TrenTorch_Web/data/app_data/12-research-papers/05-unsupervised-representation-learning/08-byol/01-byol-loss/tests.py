"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/08-byol/01-byol-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-byol-loss")
byol_loss = _module.byol_loss


import numpy as np


def test_1_identical_directions_give_zero():
    assert abs(byol_loss(np.array([1.0, 2.0]), np.array([2.0, 4.0]))) < 1e-12


def test_2_opposite_directions_give_four():
    assert abs(byol_loss(np.array([1.0, 0.0]), np.array([-1.0, 0.0])) - 4.0) < 1e-12


def test_3_orthogonal_directions_give_two():
    assert abs(byol_loss(np.array([1.0, 0.0]), np.array([0.0, 1.0])) - 2.0) < 1e-12


def test_4_scale_invariant():
    p = np.array([1.0, 3.0])
    z = np.array([2.0, 1.0])
    assert abs(byol_loss(p, z) - byol_loss(7 * p, z)) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(byol_loss(np.ones(2), np.ones(2)), float)


def test_6_does_not_mutate_inputs():
    p = np.array([1.0, 2.0])
    byol_loss(p, np.array([3.0, 4.0]))
    np.testing.assert_array_equal(p, [1.0, 2.0])

