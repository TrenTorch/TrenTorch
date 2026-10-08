"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/11-summarize/03-win-rate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-summarize-win-rate")
win_rate = _module.win_rate


import numpy as np


def test_1_always_winning_gives_one():
    assert abs(win_rate(np.array([2.0, 3.0]), np.array([1.0, 1.0])) - 1.0) < 1e-12


def test_2_all_ties_give_one_half():
    assert abs(win_rate(np.array([1.0, 1.0]), np.array([1.0, 1.0])) - 0.5) < 1e-12


def test_3_matches_a_hand_value():
    assert abs(win_rate(np.array([1.0, 2.0]), np.array([0.0, 3.0])) - 0.5) < 1e-12


def test_4_ties_count_as_half():
    assert abs(win_rate(np.array([1.0, 0.0]), np.array([1.0, 1.0])) - 0.25) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(win_rate(np.array([1.0]), np.array([0.0])), float)


def test_6_is_one_minus_loss_rate_when_no_ties():
    a = np.array([2.0, 0.0, 3.0])
    b = np.array([1.0, 1.0, 2.0])
    assert abs(win_rate(a, b) - 2 / 3) < 1e-12

