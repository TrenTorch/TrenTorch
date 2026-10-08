"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/03-dueling/01-dueling-q/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dueling-q")
dueling_q = _module.dueling_q


import numpy as np


def test_1_matches_a_hand_value():
    np.testing.assert_allclose(dueling_q(2.0, np.array([1.0, 3.0])), [1.0, 3.0])


def test_2_adding_a_constant_to_advantages_changes_nothing():
    a = dueling_q(1.0, np.array([0.0, 2.0]))
    b = dueling_q(1.0, np.array([5.0, 7.0]))
    np.testing.assert_allclose(a, b)


def test_3_mean_of_q_equals_the_value():
    q = dueling_q(4.0, np.array([-1.0, 3.0, 1.0]))
    assert abs(q.mean() - 4.0) < 1e-12


def test_4_output_has_one_entry_per_action():
    assert dueling_q(0.0, np.zeros(5)).shape == (5,)


def test_5_zero_advantage_gives_value_everywhere():
    np.testing.assert_allclose(dueling_q(3.0, np.zeros(3)), [3.0, 3.0, 3.0])


def test_6_does_not_mutate_advantages():
    A = np.array([1.0, 2.0])
    dueling_q(0.0, A)
    np.testing.assert_array_equal(A, [1.0, 2.0])

