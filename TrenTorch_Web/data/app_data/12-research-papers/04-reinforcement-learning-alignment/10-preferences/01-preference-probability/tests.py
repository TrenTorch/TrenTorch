"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/10-preferences/01-preference-probability/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-preference-probability")
preference_probability = _module.preference_probability


import math


def test_1_equal_rewards_give_one_half():
    assert abs(preference_probability(2.0, 2.0) - 0.5) < 1e-12


def test_2_large_advantage_for_a_gives_near_one():
    assert preference_probability(50.0, 0.0) > 0.999


def test_3_antisymmetric():
    assert abs(preference_probability(1.0, 3.0) + preference_probability(3.0, 1.0) - 1.0) < 1e-12


def test_4_hand_value():
    assert abs(preference_probability(1.0, 0.0) - 1 / (1 + math.exp(-1.0))) < 1e-12


def test_5_returns_a_float():
    assert isinstance(preference_probability(0.0, 0.0), float)


def test_6_is_monotone_in_the_reward_of_a():
    assert preference_probability(2.0, 0.0) > preference_probability(1.0, 0.0)

