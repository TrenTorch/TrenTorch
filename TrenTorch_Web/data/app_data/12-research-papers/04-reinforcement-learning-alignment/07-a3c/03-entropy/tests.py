"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/07-a3c/03-entropy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-a3c-entropy")
entropy = _module.entropy


import math

import numpy as np


def test_1_uniform_over_two_actions_gives_log_two():
    assert abs(entropy(np.array([0.5, 0.5])) - math.log(2.0)) < 1e-12


def test_2_deterministic_policy_has_zero_entropy():
    assert abs(entropy(np.array([1.0, 0.0, 0.0]))) < 1e-12


def test_3_uniform_over_four_actions_gives_log_four():
    assert abs(entropy(np.full(4, 0.25)) - math.log(4.0)) < 1e-12


def test_4_zero_entries_are_ignored():
    assert abs(entropy(np.array([0.5, 0.5, 0.0])) - math.log(2.0)) < 1e-12


def test_5_more_spread_means_more_entropy():
    assert entropy(np.array([0.7, 0.3])) < entropy(np.array([0.5, 0.5]))


def test_6_returns_a_python_float():
    assert isinstance(entropy(np.array([1.0])), float)

