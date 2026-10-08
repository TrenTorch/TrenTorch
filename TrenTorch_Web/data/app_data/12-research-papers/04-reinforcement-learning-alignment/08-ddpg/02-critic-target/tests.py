"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/08-ddpg/02-critic-target/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ddpg-critic-target")
ddpg_critic_target = _module.ddpg_critic_target


import numpy as np


def test_1_terminal_step_returns_the_reward():
    assert ddpg_critic_target(3.0, 0.99, 1, 100.0) == 3.0


def test_2_non_terminal_adds_discounted_value():
    assert abs(ddpg_critic_target(1.0, 0.5, 0, 4.0) - 3.0) < 1e-12


def test_3_gamma_zero_ignores_the_next_value():
    assert ddpg_critic_target(2.0, 0.0, 0, 50.0) == 2.0


def test_4_works_on_arrays():
    out = ddpg_critic_target(np.array([1.0, 0.0]), 1.0, np.array([0, 1]), np.array([2.0, 9.0]))
    np.testing.assert_allclose(out, [3.0, 0.0])


def test_5_negative_reward_is_kept():
    assert abs(ddpg_critic_target(-1.0, 0.0, 0, 5.0) - (-1.0)) < 1e-12


def test_6_returns_a_float_for_scalars():
    assert isinstance(ddpg_critic_target(1.0, 0.9, 0, 1.0), float)

