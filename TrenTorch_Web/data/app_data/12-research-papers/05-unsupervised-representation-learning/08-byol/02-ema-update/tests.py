"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/08-byol/02-ema-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-byol-ema-update")
ema_update = _module.ema_update


import numpy as np


def test_1_tau_one_copies_the_online_parameters():
    np.testing.assert_allclose(ema_update(np.array([0.0]), np.array([4.0]), 1.0), [4.0])


def test_2_tau_small_barely_moves_the_target():
    np.testing.assert_allclose(ema_update(np.array([0.0]), np.array([10.0]), 0.01), [0.1])


def test_3_keeps_the_shape():
    assert ema_update(np.zeros((2, 2)), np.ones((2, 2)), 0.5).shape == (2, 2)


def test_4_repeated_updates_converge_to_online():
    t = np.array([0.0])
    for _ in range(3000):
        t = ema_update(t, np.array([7.0]), 0.01)
    np.testing.assert_allclose(t, [7.0], atol=1e-6)


def test_5_moves_toward_online_not_away():
    out = ema_update(np.array([0.0]), np.array([1.0]), 0.3)
    assert 0.0 < out[0] < 1.0


def test_6_does_not_mutate_inputs():
    t = np.array([1.0])
    ema_update(t, np.array([2.0]), 0.5)
    np.testing.assert_array_equal(t, [1.0])

