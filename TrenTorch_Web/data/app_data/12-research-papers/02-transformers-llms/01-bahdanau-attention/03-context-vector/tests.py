"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/01-bahdanau-attention/03-context-vector/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bahdanau-context-vector")
context_vector = _module.context_vector


import numpy as np


def test_1_output_has_the_state_dimension():
    assert context_vector(np.ones(3) / 3, np.ones((3, 5))).shape == (5,)


def test_2_one_hot_weights_select_a_row():
    H = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    np.testing.assert_allclose(context_vector(np.array([0.0, 1.0, 0.0]), H), [3.0, 4.0])


def test_3_uniform_weights_average_the_states():
    H = np.array([[0.0, 2.0], [4.0, 6.0]])
    np.testing.assert_allclose(context_vector(np.array([0.5, 0.5]), H), [2.0, 4.0])


def test_4_context_lies_within_the_convex_hull():
    H = np.array([[0.0], [10.0]])
    c = context_vector(np.array([0.2, 0.8]), H)
    assert 0.0 <= c[0] <= 10.0


def test_5_matches_a_weighted_sum_by_hand():
    H = np.array([[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(context_vector(np.array([0.3, 0.7]), H), [0.3, 0.7])


def test_6_does_not_mutate_inputs():
    H = np.array([[1.0], [2.0]])
    context_vector(np.array([0.5, 0.5]), H)
    np.testing.assert_array_equal(H, [[1.0], [2.0]])

