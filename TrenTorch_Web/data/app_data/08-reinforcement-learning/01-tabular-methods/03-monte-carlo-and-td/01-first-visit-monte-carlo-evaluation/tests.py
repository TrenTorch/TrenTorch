"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

first_visit_mc = load_solution(__file__).first_visit_mc


def test_hand_computed_with_repeated_state():
    # A -> B -> A, gamma 0.5. Returns: t2 = 3, t1 = 2 + 1.5 = 3.5, t0 = 1 + 1.75 = 2.75.
    v = first_visit_mc([[("A", 1.0), ("B", 2.0), ("A", 3.0)]], 0.5)
    assert np.isclose(v["A"], 2.75)  # first visit only; every-visit would give 2.875
    assert np.isclose(v["B"], 3.5)


def test_averages_across_episodes():
    episodes = [[("S", 1.0)], [("S", 3.0)]]
    assert np.isclose(first_visit_mc(episodes, 0.9)["S"], 2.0)


def test_gamma_one_is_the_plain_sum():
    v = first_visit_mc([[("A", 1.0), ("B", 2.0), ("C", 3.0)]], 1.0)
    assert v == {"A": 6.0, "B": 5.0, "C": 3.0}


def test_gamma_zero_is_the_immediate_reward():
    v = first_visit_mc([[("A", 1.0), ("B", 2.0)]], 0.0)
    assert v == {"A": 1.0, "B": 2.0}


def test_only_visited_states_appear():
    assert set(first_visit_mc([[("A", 0.0), ("B", 0.0)]], 0.9)) == {"A", "B"}


def test_a_state_counts_once_per_episode():
    # In the second episode "A" appears twice; only its first return counts.
    episodes = [[("A", 1.0)], [("A", 1.0), ("A", 10.0)]]
    # episode 2 first-visit return = 1 + 10 = 11 (gamma 1); mean(1, 11) = 6.
    assert np.isclose(first_visit_mc(episodes, 1.0)["A"], 6.0)


def test_empty_input_gives_empty_dict():
    assert first_visit_mc([], 0.9) == {}


def test_values_are_python_floats():
    assert isinstance(first_visit_mc([[("A", 1.0)]], 0.9)["A"], float)
