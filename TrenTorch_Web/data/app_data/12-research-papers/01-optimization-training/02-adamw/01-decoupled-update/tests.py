"""
pytest data/app_data/12-research-papers/01-optimization-and-training/02-adamw/01-decoupled-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adamw-decoupled-update")
adamw_update = _module.adamw_update


import numpy as np


def test_1_hand_value_with_decay():
    out = adamw_update(np.array([1.0]), np.array([1.0]), np.array([1.0]), 0.1, 0.5, 0.0)
    np.testing.assert_allclose(out, [0.85])


def test_2_zero_decay_is_plain_adam():
    out = adamw_update(np.array([2.0]), np.array([1.0]), np.array([4.0]), 0.1, 0.0, 0.0)
    np.testing.assert_allclose(out, [2.0 - 0.1 * 0.5])


def test_3_zero_lr_leaves_weights():
    w = np.array([3.0, -2.0])
    np.testing.assert_allclose(adamw_update(w, np.ones(2), np.ones(2), 0.0, 0.5, 1e-8), w)


def test_4_decay_shrinks_weights_with_zero_gradient():
    w = np.array([2.0])
    out = adamw_update(w, np.zeros(1), np.ones(1), 0.1, 0.5, 0.0)
    np.testing.assert_allclose(out, [2.0 - 0.1 * 0.5 * 2.0])


def test_5_keeps_the_shape():
    assert adamw_update(np.ones((2, 3)), np.ones((2, 3)), np.ones((2, 3)), 0.1, 0.1, 1e-8).shape == (2, 3)


def test_6_does_not_mutate_inputs():
    w = np.array([1.0])
    adamw_update(w, np.array([1.0]), np.array([1.0]), 0.1, 0.5, 0.0)
    np.testing.assert_array_equal(w, [1.0])

