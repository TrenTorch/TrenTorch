"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/02-catboost/02-target-statistic/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-catboost-target-statistic")
target_statistic = _module.target_statistic


def test_1_no_history_returns_the_prior():
    assert abs(target_statistic(0.0, 0, 0.3) - 0.3) < 1e-12


def test_2_zero_prior_weight_gives_the_plain_mean():
    assert abs(target_statistic(3.0, 4, 0.5, a=0.0) - 0.75) < 1e-12


def test_3_matches_a_hand_value():
    assert abs(target_statistic(2.0, 3, 0.5, a=1.0) - (2.5 / 4.0)) < 1e-12


def test_4_large_counts_approach_the_empirical_mean():
    assert abs(target_statistic(900.0, 1000, 0.1) - 0.9) < 0.01


def test_5_prior_pulls_small_counts_toward_it():
    assert abs(target_statistic(1.0, 1, 0.0) - 0.5) < 1e-12


def test_6_returns_a_float():
    assert isinstance(target_statistic(1.0, 2, 0.5), float)

