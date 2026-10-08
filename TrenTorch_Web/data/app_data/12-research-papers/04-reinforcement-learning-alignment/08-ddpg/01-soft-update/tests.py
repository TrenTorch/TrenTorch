"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/08-ddpg/01-soft-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ddpg-soft-update")
soft_update = _module.soft_update


import numpy as np


def test_1_tau_zero_keeps_the_target():
    np.testing.assert_allclose(soft_update(np.array([1.0]), np.array([9.0]), 0.0), [1.0])


def test_2_tau_one_copies_the_online_network():
    np.testing.assert_allclose(soft_update(np.array([1.0]), np.array([9.0]), 1.0), [9.0])


def test_3_small_tau_moves_slightly():
    out = soft_update(np.array([0.0]), np.array([10.0]), 0.1)
    np.testing.assert_allclose(out, [1.0])


def test_4_keeps_the_shape():
    assert soft_update(np.zeros((2, 3)), np.ones((2, 3)), 0.5).shape == (2, 3)


def test_5_repeated_updates_converge_to_online():
    t = np.array([0.0])
    o = np.array([4.0])
    for _ in range(500):
        t = soft_update(t, o, 0.05)
    np.testing.assert_allclose(t, o, atol=1e-6)


def test_6_does_not_mutate_inputs():
    t = np.array([1.0])
    soft_update(t, np.array([2.0]), 0.5)
    np.testing.assert_array_equal(t, [1.0])

