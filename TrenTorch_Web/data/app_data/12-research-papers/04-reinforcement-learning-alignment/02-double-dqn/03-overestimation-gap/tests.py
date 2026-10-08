"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/02-double-dqn/03-overestimation-gap/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-double-dqn-overestimation-gap")
overestimation_gap = _module.overestimation_gap


def test_1_matches_a_hand_value():
    assert abs(overestimation_gap(3.0, 1.0) - 2.0) < 1e-12


def test_2_equal_targets_give_zero_gap():
    assert overestimation_gap(4.0, 4.0) == 0.0


def test_3_negative_gap_is_possible():
    assert overestimation_gap(1.0, 2.0) < 0


def test_4_returns_a_python_float():
    assert isinstance(overestimation_gap(1.0, 0.0), float)


def test_5_is_antisymmetric():
    assert overestimation_gap(5.0, 2.0) == -overestimation_gap(2.0, 5.0)


def test_6_zero_targets_give_zero_gap():
    assert overestimation_gap(0.0, 0.0) == 0.0

