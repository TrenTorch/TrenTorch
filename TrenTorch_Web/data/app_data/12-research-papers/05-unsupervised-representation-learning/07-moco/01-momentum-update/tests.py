"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/07-moco/01-momentum-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-moco-momentum-update")
momentum_update = _module.momentum_update


import numpy as np


def test_1_m_one_keeps_the_key_encoder():
    np.testing.assert_allclose(momentum_update(np.array([1.0]), np.array([9.0]), 1.0), [1.0])


def test_2_m_zero_copies_the_query_encoder():
    np.testing.assert_allclose(momentum_update(np.array([1.0]), np.array([9.0]), 0.0), [9.0])


def test_3_hand_value():
    assert abs(momentum_update(np.array([0.0]), np.array([10.0]), 0.9)[0] - 1.0) < 1e-12


def test_4_keeps_the_shape():
    assert momentum_update(np.zeros((2, 3)), np.ones((2, 3)), 0.5).shape == (2, 3)


def test_5_repeated_updates_track_the_query():
    k = np.array([0.0])
    q_ = np.array([5.0])
    for _ in range(2000):
        k = momentum_update(k, q_, 0.99)
    np.testing.assert_allclose(k, q_, atol=1e-6)


def test_6_does_not_mutate_inputs():
    k = np.array([1.0])
    momentum_update(k, np.array([2.0]), 0.5)
    np.testing.assert_array_equal(k, [1.0])

