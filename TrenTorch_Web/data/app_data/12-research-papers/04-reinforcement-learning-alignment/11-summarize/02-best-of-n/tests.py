"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/11-summarize/02-best-of-n/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-summarize-best-of-n")
best_of_n_index = _module.best_of_n_index


import numpy as np


def test_1_picks_the_highest_score():
    assert best_of_n_index(np.array([0.1, 0.9, 0.5])) == 1


def test_2_ties_pick_the_first():
    assert best_of_n_index(np.array([2.0, 2.0])) == 0


def test_3_returns_a_python_int():
    assert isinstance(best_of_n_index(np.array([1.0, 3.0])), int)


def test_4_single_candidate():
    assert best_of_n_index(np.array([-4.0])) == 0


def test_5_negative_scores_are_compared_correctly():
    assert best_of_n_index(np.array([-3.0, -1.0, -2.0])) == 1


def test_6_does_not_mutate_scores():
    s = np.array([1.0, 2.0])
    best_of_n_index(s)
    np.testing.assert_array_equal(s, [1.0, 2.0])

