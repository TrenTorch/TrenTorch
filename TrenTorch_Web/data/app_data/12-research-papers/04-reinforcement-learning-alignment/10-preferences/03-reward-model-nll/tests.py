"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/10-preferences/03-reward-model-nll/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-preference-reward-nll")
reward_model_nll = _module.reward_model_nll


import math


def test_1_uncertain_model_gives_log_two():
    assert abs(reward_model_nll(1, 0.0, 0.0) - math.log(2.0)) < 1e-12


def test_2_confident_correct_prediction_has_small_loss():
    assert reward_model_nll(1, 30.0, 0.0) < 1e-6


def test_3_confident_wrong_prediction_has_large_loss():
    assert reward_model_nll(1, 0.0, 30.0) > 20.0


def test_4_label_zero_rewards_b_being_preferred():
    assert reward_model_nll(0, 0.0, 30.0) < 1e-6


def test_5_returns_a_python_float():
    assert isinstance(reward_model_nll(1, 1.0, 0.0), float)


def test_6_matches_a_hand_value():
    p = 1 / (1 + math.exp(-1.0))
    assert abs(reward_model_nll(1, 1.0, 0.0) - (-math.log(p))) < 1e-12

