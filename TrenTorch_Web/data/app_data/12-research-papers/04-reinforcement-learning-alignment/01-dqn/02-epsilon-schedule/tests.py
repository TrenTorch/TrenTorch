"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/01-dqn/02-epsilon-schedule/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dqn-epsilon-schedule")
epsilon_schedule = _module.epsilon_schedule


def test_1_step_zero_gives_start():
    assert abs(epsilon_schedule(0, 1.0, 0.1, 100) - 1.0) < 1e-12


def test_2_after_decay_gives_end():
    assert epsilon_schedule(100, 1.0, 0.1, 100) == 0.1
    assert epsilon_schedule(500, 1.0, 0.1, 100) == 0.1


def test_3_midpoint_is_the_average():
    assert abs(epsilon_schedule(50, 1.0, 0.0, 100) - 0.5) < 1e-12


def test_4_is_nonincreasing_when_start_exceeds_end():
    values = [epsilon_schedule(s, 1.0, 0.1, 10) for s in range(12)]
    assert all(a >= b for a, b in zip(values, values[1:]))


def test_5_returns_a_float():
    assert isinstance(epsilon_schedule(3, 1.0, 0.1, 10), float)


def test_6_decay_quarter_way():
    assert abs(epsilon_schedule(25, 0.8, 0.2, 100) - 0.65) < 1e-12

