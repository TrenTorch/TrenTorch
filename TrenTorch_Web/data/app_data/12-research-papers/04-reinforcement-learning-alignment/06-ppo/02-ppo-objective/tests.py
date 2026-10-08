"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/06-ppo/02-ppo-objective/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ppo-objective-batch")
ppo_objective = _module.ppo_objective


import numpy as np


def test_1_unit_ratios_give_the_mean_advantage():
    assert abs(ppo_objective(np.ones(3), np.array([1.0, 2.0, 3.0]), 0.2) - 2.0) < 1e-12


def test_2_large_ratio_with_positive_advantage_is_clipped():
    assert abs(ppo_objective(np.array([1.5]), np.array([1.0]), 0.2) - 1.2) < 1e-12


def test_3_large_ratio_with_negative_advantage_is_not_clipped():
    assert abs(ppo_objective(np.array([1.5]), np.array([-1.0]), 0.2) - (-1.5)) < 1e-12


def test_4_mixed_batch_averages_correctly():
    out = ppo_objective(np.array([1.5, 1.0]), np.array([1.0, 2.0]), 0.2)
    assert abs(out - (1.2 + 2.0) / 2) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(ppo_objective(np.ones(2), np.ones(2), 0.1), float)


def test_6_does_not_mutate_inputs():
    r = np.array([1.2])
    ppo_objective(r, np.array([1.0]), 0.2)
    np.testing.assert_array_equal(r, [1.2])

