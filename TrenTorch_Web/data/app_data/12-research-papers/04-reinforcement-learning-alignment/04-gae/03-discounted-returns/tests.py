"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/04-gae/03-discounted-returns/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gae-discounted-returns")
discounted_returns = _module.discounted_returns


import numpy as np


def test_1_gamma_one_gives_suffix_sums():
    np.testing.assert_allclose(discounted_returns(np.array([1.0, 2.0, 3.0]), 1.0), [6.0, 5.0, 3.0])


def test_2_gamma_zero_returns_the_rewards():
    r = np.array([4.0, 5.0])
    np.testing.assert_allclose(discounted_returns(r, 0.0), r)


def test_3_matches_a_hand_computed_case():
    np.testing.assert_allclose(discounted_returns(np.array([1.0, 1.0, 1.0]), 0.5), [1.75, 1.5, 1.0])


def test_4_last_return_is_the_last_reward():
    assert discounted_returns(np.array([0.0, 7.0]), 0.9)[-1] == 7.0


def test_5_output_length_matches_input():
    assert len(discounted_returns(np.ones(5), 0.9)) == 5


def test_6_does_not_mutate_input():
    r = np.array([1.0, 2.0])
    discounted_returns(r, 0.5)
    np.testing.assert_array_equal(r, [1.0, 2.0])

