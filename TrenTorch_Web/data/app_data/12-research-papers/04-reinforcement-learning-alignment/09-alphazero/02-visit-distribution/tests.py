"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/09-alphazero/02-visit-distribution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-alphazero-visit-distribution")
visit_distribution = _module.visit_distribution


import numpy as np


def test_1_tau_one_is_proportional_to_counts():
    np.testing.assert_allclose(visit_distribution(np.array([1.0, 3.0]), 1.0), [0.25, 0.75])


def test_2_hand_value_for_tau_half():
    np.testing.assert_allclose(visit_distribution(np.array([1.0, 2.0]), 0.5), [0.2, 0.8])


def test_3_small_tau_concentrates_on_the_most_visited_move():
    out = visit_distribution(np.array([2.0, 1.0]), 0.001)
    assert out[0] > 0.999


def test_4_sums_to_one():
    assert abs(visit_distribution(np.array([2.0, 5.0, 1.0]), 0.7).sum() - 1.0) < 1e-12


def test_5_equal_counts_give_uniform():
    np.testing.assert_allclose(visit_distribution(np.array([4.0, 4.0]), 2.0), [0.5, 0.5])


def test_6_does_not_mutate_counts():
    c = np.array([1.0, 2.0])
    visit_distribution(c, 1.0)
    np.testing.assert_array_equal(c, [1.0, 2.0])

