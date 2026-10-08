"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/03-dueling/02-centered-advantage/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dueling-centered-advantage")
centered_advantage = _module.centered_advantage


import numpy as np


def test_1_centered_advantages_sum_to_zero():
    assert abs(centered_advantage(np.array([1.0, 2.0, 6.0])).sum()) < 1e-12


def test_2_matches_a_hand_value():
    np.testing.assert_allclose(centered_advantage(np.array([1.0, 3.0])), [-1.0, 1.0])


def test_3_constant_advantages_become_zero():
    np.testing.assert_allclose(centered_advantage(np.array([4.0, 4.0])), [0.0, 0.0])


def test_4_keeps_the_shape():
    assert centered_advantage(np.ones(6)).shape == (6,)


def test_5_order_of_actions_is_preserved():
    out = centered_advantage(np.array([0.0, 5.0, 2.0]))
    assert out[1] > out[2] > out[0]


def test_6_does_not_mutate_input():
    A = np.array([1.0, 3.0])
    centered_advantage(A)
    np.testing.assert_array_equal(A, [1.0, 3.0])

