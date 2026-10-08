"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/12-bayesian-optimization/03-probability-improvement/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bo-probability-improvement")
probability_of_improvement = _module.probability_of_improvement


import math


def test_1_mean_equal_to_best_gives_one_half():
    assert abs(probability_of_improvement(1.0, 1.0, 1.0) - 0.5) < 1e-12


def test_2_mean_well_below_best_gives_near_one():
    assert probability_of_improvement(-100.0, 1.0, 0.0) > 0.999


def test_3_mean_well_above_best_gives_near_zero():
    assert probability_of_improvement(100.0, 1.0, 0.0) < 0.001


def test_4_hand_value_at_z_one():
    assert abs(probability_of_improvement(0.0, 1.0, 1.0) - 0.8413447460685429) < 1e-9


def test_5_is_monotone_decreasing_in_mu():
    assert probability_of_improvement(0.0, 1.0, 0.0) > probability_of_improvement(1.0, 1.0, 0.0)


def test_6_returns_a_float_between_zero_and_one():
    p = probability_of_improvement(0.3, 0.7, 0.5)
    assert isinstance(p, float) and 0.0 <= p <= 1.0

