"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/03-dueling/03-dueling-argmax/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dueling-q-argmax")
dueling_argmax = _module.dueling_argmax


import numpy as np


def test_1_greedy_action_matches_the_advantage_argmax():
    A = np.array([0.5, 2.0, 1.0])
    assert dueling_argmax(3.0, A) == int(np.argmax(A))


def test_2_value_does_not_change_the_choice():
    A = np.array([0.5, 2.0, 1.0])
    assert dueling_argmax(-100.0, A) == dueling_argmax(100.0, A)


def test_3_returns_a_python_int():
    assert isinstance(dueling_argmax(0.0, np.array([1.0, 2.0])), int)


def test_4_single_action():
    assert dueling_argmax(1.0, np.array([7.0])) == 0


def test_5_ties_pick_the_first_action():
    assert dueling_argmax(0.0, np.array([1.0, 1.0])) == 0


def test_6_does_not_mutate_advantages():
    A = np.array([1.0, 3.0])
    dueling_argmax(0.0, A)
    np.testing.assert_array_equal(A, [1.0, 3.0])

