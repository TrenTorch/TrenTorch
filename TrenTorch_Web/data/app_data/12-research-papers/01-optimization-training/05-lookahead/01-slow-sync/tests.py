"""
pytest data/app_data/12-research-papers/01-optimization-and-training/05-lookahead/01-slow-sync/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lookahead-slow-sync")
lookahead_sync = _module.lookahead_sync


import numpy as np


def test_1_halfway_move():
    assert abs(lookahead_sync(0.0, 1.0, 0.5) - 0.5) < 1e-12


def test_2_alpha_one_copies_fast_weights():
    np.testing.assert_allclose(lookahead_sync(np.zeros(2), np.array([3.0, 4.0]), 1.0), [3.0, 4.0])


def test_3_alpha_zero_keeps_slow_weights():
    np.testing.assert_allclose(lookahead_sync(np.array([2.0]), np.array([9.0]), 0.0), [2.0])


def test_4_no_change_when_fast_equals_slow():
    s = np.array([1.0, -1.0])
    np.testing.assert_allclose(lookahead_sync(s, s.copy(), 0.7), s)


def test_5_keeps_the_shape():
    assert lookahead_sync(np.zeros((2, 3)), np.ones((2, 3)), 0.5).shape == (2, 3)


def test_6_does_not_mutate_inputs():
    s = np.zeros(1)
    lookahead_sync(s, np.ones(1), 0.5)
    np.testing.assert_array_equal(s, [0.0])

