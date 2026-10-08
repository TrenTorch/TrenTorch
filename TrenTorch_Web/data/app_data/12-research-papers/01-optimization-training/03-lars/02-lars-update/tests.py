"""
pytest data/app_data/12-research-papers/01-optimization-and-training/03-lars/02-lars-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lars-update")
lars_update = _module.lars_update


import numpy as np


def test_1_hand_value():
    out = lars_update(np.array([3.0, 4.0]), np.array([0.6, 0.8]), 0.1, 0.5, 0.0)
    np.testing.assert_allclose(out, [2.85, 3.8])


def test_2_zero_lr_leaves_weights():
    w = np.array([1.0, 2.0])
    np.testing.assert_allclose(lars_update(w, np.ones(2), 0.0, 0.5, 0.1), w)


def test_3_update_direction_opposes_gradient():
    w = np.array([3.0, 4.0])
    g = np.array([0.6, 0.8])
    out = lars_update(w, g, 0.1, 0.5, 0.0)
    assert np.all((w - out) * g >= 0)


def test_4_keeps_the_shape():
    assert lars_update(np.ones((2, 2)), np.ones((2, 2)), 0.1, 0.5, 0.0).shape == (2, 2)


def test_5_decay_pulls_weights_toward_zero():
    w = np.array([3.0, 4.0])
    out_decay = lars_update(w, np.zeros(2), 0.1, 0.5, 0.2)
    assert np.linalg.norm(out_decay) < np.linalg.norm(w)


def test_6_does_not_mutate_weights():
    w = np.array([3.0, 4.0])
    lars_update(w, np.array([0.6, 0.8]), 0.1, 0.5, 0.0)
    np.testing.assert_array_equal(w, [3.0, 4.0])

