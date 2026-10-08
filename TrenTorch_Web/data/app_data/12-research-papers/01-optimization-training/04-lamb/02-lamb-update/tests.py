"""
pytest data/app_data/12-research-papers/01-optimization-and-training/04-lamb/02-lamb-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lamb-update")
lamb_update = _module.lamb_update


import numpy as np


def test_1_hand_value():
    np.testing.assert_allclose(lamb_update(np.array([3.0, 4.0]), np.array([0.6, 0.8]), 0.1), [2.7, 3.6])


def test_2_zero_lr_leaves_weights():
    w = np.array([1.0, 2.0])
    np.testing.assert_allclose(lamb_update(w, np.array([1.0, 0.0]), 0.0), w)


def test_3_step_length_is_lr_times_weight_norm():
    w = np.array([3.0, 4.0])
    r = np.array([0.6, 0.8])
    step = np.linalg.norm(w - lamb_update(w, r, 0.1))
    assert abs(step - 0.1 * 5.0) < 1e-12


def test_4_keeps_the_shape():
    assert lamb_update(np.ones((2, 3)), np.ones((2, 3)), 0.1).shape == (2, 3)


def test_5_moves_against_the_direction():
    w = np.array([3.0, 4.0])
    r = np.array([0.6, 0.8])
    assert np.all((w - lamb_update(w, r, 0.1)) * r >= 0)


def test_6_does_not_mutate_weights():
    w = np.array([3.0, 4.0])
    lamb_update(w, np.array([0.6, 0.8]), 0.1)
    np.testing.assert_array_equal(w, [3.0, 4.0])

