"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/01-bahdanau-attention/01-additive-scores/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bahdanau-additive-scores")
additive_scores = _module.additive_scores


import numpy as np


def test_1_one_score_per_encoder_state():
    scores = additive_scores(np.ones(2), np.ones((5, 3)), np.ones((4, 2)), np.ones((4, 3)), np.ones(4))
    assert scores.shape == (5,)


def test_2_zero_weights_give_zero_scores():
    scores = additive_scores(np.ones(2), np.ones((3, 2)), np.zeros((4, 2)), np.zeros((4, 2)), np.ones(4))
    np.testing.assert_allclose(scores, 0.0)


def test_3_matches_a_hand_computed_case():
    # tanh(0 + 0) = 0; tanh(0 + 1) = tanh(1)
    scores = additive_scores(np.array([0.0]), np.array([[0.0], [1.0]]), np.array([[1.0]]), np.array([[1.0]]), np.array([1.0]))
    np.testing.assert_allclose(scores, [0.0, np.tanh(1.0)])


def test_4_scores_scale_linearly_with_v():
    args = (np.array([0.5]), np.array([[1.0], [2.0]]), np.array([[1.0]]), np.array([[1.0]]))
    a = additive_scores(*args, np.array([1.0]))
    b = additive_scores(*args, np.array([2.0]))
    np.testing.assert_allclose(b, 2 * a)


def test_5_scores_are_bounded_by_the_norm_of_v():
    rng = np.random.default_rng(0)
    scores = additive_scores(rng.normal(size=3), rng.normal(size=(6, 2)), rng.normal(size=(5, 3)), rng.normal(size=(5, 2)), np.ones(5))
    assert np.all(np.abs(scores) <= 5.0)


def test_6_does_not_mutate_inputs():
    H = np.array([[1.0], [2.0]])
    additive_scores(np.array([0.0]), H, np.array([[1.0]]), np.array([[1.0]]), np.array([1.0]))
    np.testing.assert_array_equal(H, [[1.0], [2.0]])

