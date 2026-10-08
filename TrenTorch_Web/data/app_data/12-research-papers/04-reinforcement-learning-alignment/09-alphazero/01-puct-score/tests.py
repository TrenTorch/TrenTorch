"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/09-alphazero/01-puct-score/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-alphazero-puct")
puct_score = _module.puct_score


import math


def test_1_no_parent_visits_gives_only_the_value():
    assert puct_score(0.5, 0.2, 0, 0, 1.0) == 0.5


def test_2_matches_a_hand_value():
    assert abs(puct_score(0.5, 0.2, 4, 0, 1.0) - 0.9) < 1e-12


def test_3_higher_prior_gives_higher_score():
    assert puct_score(0.0, 0.5, 9, 0, 1.0) > puct_score(0.0, 0.1, 9, 0, 1.0)


def test_4_more_child_visits_lower_the_bonus():
    assert puct_score(0.0, 0.5, 9, 9, 1.0) < puct_score(0.0, 0.5, 9, 0, 1.0)


def test_5_returns_a_float():
    assert isinstance(puct_score(0.0, 0.5, 4, 1, 1.0), float)


def test_6_bonus_scales_with_exploration_constant():
    base = puct_score(0.0, 1.0, 4, 0, 1.0)
    doubled = puct_score(0.0, 1.0, 4, 0, 2.0)
    assert abs(doubled - 2 * base) < 1e-12

