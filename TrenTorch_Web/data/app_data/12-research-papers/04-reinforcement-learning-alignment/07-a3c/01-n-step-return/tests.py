"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/07-a3c/01-n-step-return/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-a3c-n-step-return")
n_step_return = _module.n_step_return


def test_1_no_rewards_returns_the_bootstrap():
    assert abs(n_step_return([], 3.0, 0.9) - 3.0) < 1e-12


def test_2_matches_a_hand_value():
    # 1 + 0.5 * (1 + 0.5 * 0) = 1.5
    assert abs(n_step_return([1.0, 1.0], 0.0, 0.5) - 1.5) < 1e-12


def test_3_gamma_one_sums_rewards_and_bootstrap():
    assert abs(n_step_return([1.0, 2.0], 4.0, 1.0) - 7.0) < 1e-12


def test_4_gamma_zero_returns_the_first_reward():
    assert abs(n_step_return([9.0, 100.0], 50.0, 0.0) - 9.0) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(n_step_return([1.0], 0.0, 0.9), float)


def test_6_does_not_mutate_rewards():
    r = [1.0, 2.0]
    n_step_return(r, 0.0, 0.5)
    assert r == [1.0, 2.0]

