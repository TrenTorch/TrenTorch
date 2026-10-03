"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

td0_update = load_solution(__file__).td0_update


def test_hand_computed_update():
    V = np.array([1.0, 4.0])
    # target = 2 + 0.5 * 4 = 4; delta = 3; V[0] = 1 + 0.1 * 3
    new = td0_update(V, 0, 2.0, 1, 0.1, 0.5)
    assert np.allclose(new, [1.3, 4.0])


def test_terminal_transition_ignores_next_value():
    V = np.array([1.0, 100.0])
    new = td0_update(V, 0, 2.0, 1, 0.5, 0.9, done=True)
    assert np.isclose(new[0], 1.0 + 0.5 * (2.0 - 1.0))


def test_alpha_one_jumps_to_target():
    V = np.array([0.0, 10.0])
    assert np.isclose(td0_update(V, 0, 1.0, 1, 1.0, 0.9)[0], 1.0 + 0.9 * 10.0)


def test_alpha_zero_changes_nothing():
    V = np.array([3.0, 5.0])
    assert np.allclose(td0_update(V, 0, 9.0, 1, 0.0, 0.9), V)


def test_input_is_not_modified():
    V = np.array([1.0, 2.0])
    td0_update(V, 0, 1.0, 1, 0.5, 0.9)
    assert V.tolist() == [1.0, 2.0]


def test_only_the_visited_state_changes():
    V = np.array([1.0, 2.0, 3.0])
    new = td0_update(V, 1, 1.0, 2, 0.5, 0.9)
    assert new[0] == 1.0 and new[2] == 3.0 and new[1] != 2.0


def test_converges_on_a_deterministic_chain():
    # State 0 -> state 1 (reward 1), state 1 -> terminal (reward 2), gamma 1.
    V = np.zeros(2)
    for _ in range(500):
        V = td0_update(V, 1, 2.0, 1, 0.1, 1.0, done=True)
        V = td0_update(V, 0, 1.0, 1, 0.1, 1.0)
    assert np.allclose(V, [3.0, 2.0], atol=1e-3)
