"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/10-adaptive-computation-time/02-ponder-cost/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-act-ponder-cost")
act_ponder_cost = _module.act_ponder_cost


def test_1_hand_value():
    assert abs(act_ponder_cost(3, 0.01) - 0.03) < 1e-12


def test_2_zero_weight_costs_nothing():
    assert act_ponder_cost(10, 0.0) == 0.0


def test_3_more_steps_cost_more():
    assert act_ponder_cost(5, 0.1) > act_ponder_cost(2, 0.1)


def test_4_one_step_costs_tau():
    assert abs(act_ponder_cost(1, 0.25) - 0.25) < 1e-12


def test_5_linear_in_steps():
    assert abs(act_ponder_cost(4, 0.5) - 2 * act_ponder_cost(2, 0.5)) < 1e-12


def test_6_returns_a_float():
    assert isinstance(act_ponder_cost(2, 1.0), float)

