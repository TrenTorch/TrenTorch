"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/04-gae/01-td-residuals/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gae-td-residuals")
td_residuals = _module.td_residuals


import numpy as np


def test_1_single_step_residual():
    out = td_residuals([1.0], [0.5], 0.9, 2.0)
    np.testing.assert_allclose(out, [1.0 + 0.9 * 2.0 - 0.5])


def test_2_gamma_zero_is_reward_minus_value():
    out = td_residuals([1.0, 2.0], [0.5, 1.0], 0.0, 9.0)
    np.testing.assert_allclose(out, [0.5, 1.0])


def test_3_bootstraps_from_the_next_value():
    out = td_residuals([0.0, 0.0], [1.0, 2.0], 1.0, 3.0)
    np.testing.assert_allclose(out, [2.0 - 1.0, 3.0 - 2.0])


def test_4_output_length_matches_rewards():
    assert len(td_residuals([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], 0.5, 0.0)) == 3


def test_5_zero_everything_gives_zero():
    np.testing.assert_allclose(td_residuals([0.0], [0.0], 0.9, 0.0), [0.0])


def test_6_does_not_mutate_inputs():
    v = np.array([1.0, 2.0])
    td_residuals(np.array([0.0, 0.0]), v, 0.5, 0.0)
    np.testing.assert_array_equal(v, [1.0, 2.0])

