"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/12-bayesian-optimization/01-expected-improvement/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ei-expected-improvement")
expected_improvement = _module.expected_improvement


import math


def test_1_at_the_mean_equal_to_best_ei_is_sigma_times_phi_zero():
    assert abs(expected_improvement(0.0, 1.0, 0.0) - 1.0 / math.sqrt(2.0 * math.pi)) < 1e-12


def test_2_hand_value_at_z_one():
    # z = 1: (best - mu) * Phi(1) + sigma * phi(1) = 1 * 0.8413447 + 0.2419707
    assert abs(expected_improvement(1.0, 1.0, 2.0) - 1.0833154705) < 1e-6


def test_3_far_worse_candidate_has_near_zero_ei():
    assert expected_improvement(100.0, 1.0, 0.0) < 1e-12


def test_4_is_nonnegative():
    for mu in [-2.0, 0.0, 2.0]:
        assert expected_improvement(mu, 1.0, 0.0) >= -1e-12


def test_5_more_uncertainty_at_equal_mean_gives_more_ei():
    assert expected_improvement(0.0, 2.0, 0.0) > expected_improvement(0.0, 1.0, 0.0)


def test_6_returns_a_float():
    assert isinstance(expected_improvement(0.0, 1.0, 1.0), float)

