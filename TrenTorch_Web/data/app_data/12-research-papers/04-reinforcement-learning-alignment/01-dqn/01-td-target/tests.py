"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/01-dqn/01-td-target/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dqn-td-target")
td_target = _module.td_target


def test_1_terminal_transition_returns_only_the_reward():
    assert td_target(2.0, 0.9, 100.0, 1) == 2.0


def test_2_non_terminal_adds_discounted_next_value():
    assert abs(td_target(1.0, 0.9, 10.0, 0) - 10.0) < 1e-12


def test_3_gamma_zero_ignores_the_future():
    assert td_target(3.0, 0.0, 50.0, 0) == 3.0


def test_4_works_on_arrays():
    import numpy as np

    out = td_target(np.array([1.0, 0.0]), 0.5, np.array([2.0, 4.0]), np.array([0, 1]))
    np.testing.assert_allclose(out, [2.0, 0.0])


def test_5_negative_rewards_are_kept():
    assert abs(td_target(-1.0, 1.0, 1.0, 0) - 0.0) < 1e-12


def test_6_returns_a_float_for_scalars():
    assert isinstance(td_target(1.0, 0.5, 1.0, 0), float)

