"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

update_action_value = load_solution(__file__).update_action_value


def test_first_reward_becomes_the_estimate():
    q, n = update_action_value(np.zeros(3), np.zeros(3, dtype=int), 1, 4.0)
    assert np.allclose(q, [0.0, 4.0, 0.0])
    assert n.tolist() == [0, 1, 0]


def test_sequence_equals_sample_mean():
    rewards = [1.0, 5.0, 3.0, 7.0, 4.0]
    q, n = np.zeros(2), np.zeros(2, dtype=int)
    for r in rewards:
        q, n = update_action_value(q, n, 0, r)
    assert np.isclose(q[0], np.mean(rewards))
    assert n[0] == len(rewards)


def test_other_arms_are_untouched():
    q, n = update_action_value(np.array([1.0, 2.0, 3.0]), np.array([4, 5, 6]), 2, 9.0)
    assert q[0] == 1.0 and q[1] == 2.0
    assert n[0] == 4 and n[1] == 5


def test_inputs_are_not_modified():
    q0, n0 = np.array([1.0, 2.0]), np.array([3, 4])
    update_action_value(q0, n0, 0, 10.0)
    assert q0.tolist() == [1.0, 2.0] and n0.tolist() == [3, 4]


def test_hand_computed_update():
    # q = 2.0 after 3 pulls; a reward of 6 gives 2 + (6 - 2) / 4 = 3.
    q, n = update_action_value(np.array([2.0]), np.array([3]), 0, 6.0)
    assert np.isclose(q[0], 3.0) and n[0] == 4


def test_each_arm_tracks_its_own_mean():
    q, n = np.zeros(2), np.zeros(2, dtype=int)
    for arm, r in [(0, 1.0), (1, 10.0), (0, 3.0), (1, 20.0)]:
        q, n = update_action_value(q, n, arm, r)
    assert np.allclose(q, [2.0, 15.0])
