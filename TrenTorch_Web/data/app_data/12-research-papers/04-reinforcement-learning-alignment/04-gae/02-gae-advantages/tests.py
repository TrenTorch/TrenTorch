"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/04-gae/02-gae-advantages/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gae-advantages")
gae_advantages = _module.gae_advantages


import numpy as np


def test_1_lambda_zero_returns_the_residuals():
    d = np.array([1.0, 2.0, 3.0])
    np.testing.assert_allclose(gae_advantages(d, 0.9, 0.0), d)


def test_2_lambda_one_gamma_one_gives_suffix_sums():
    d = np.array([1.0, 2.0, 3.0])
    np.testing.assert_allclose(gae_advantages(d, 1.0, 1.0), [6.0, 5.0, 3.0])


def test_3_matches_a_hand_computed_case():
    # A_1 = 2; A_0 = 1 + 0.5 * 0.5 * 2 = 1.5
    np.testing.assert_allclose(gae_advantages(np.array([1.0, 2.0]), 0.5, 0.5), [1.5, 2.0])


def test_4_output_shape_matches_input():
    assert gae_advantages(np.ones(7), 0.99, 0.95).shape == (7,)


def test_5_last_entry_is_the_last_residual():
    assert abs(gae_advantages(np.array([0.0, 4.0]), 0.9, 0.9)[-1] - 4.0) < 1e-12


def test_6_does_not_mutate_input():
    d = np.array([1.0, 1.0])
    gae_advantages(d, 0.9, 0.9)
    np.testing.assert_array_equal(d, [1.0, 1.0])

