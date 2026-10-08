"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/08-chinchilla/03-optimal-params-for-budget/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-chinchilla-optimal-params")
optimal_params_for_budget = _module.optimal_params_for_budget


import math


def test_1_unit_budget_gives_one_over_sqrt_120():
    assert abs(optimal_params_for_budget(120.0) - 1.0) < 1e-12


def test_2_inverts_the_chinchilla_budget_relation():
    N = 4e9
    C = 6 * N * (20 * N)
    assert abs(optimal_params_for_budget(C) - N) / N < 1e-9


def test_3_larger_budget_gives_larger_model():
    assert optimal_params_for_budget(1e22) > optimal_params_for_budget(1e20)


def test_4_scales_as_square_root_of_budget():
    assert abs(optimal_params_for_budget(4e20) - 2 * optimal_params_for_budget(1e20)) < 1e-3


def test_5_returns_a_float():
    assert isinstance(optimal_params_for_budget(1e20), float)


def test_6_matches_a_hand_value():
    assert abs(optimal_params_for_budget(1.2e20) - 1e9) < 1e-3

