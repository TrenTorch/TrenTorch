"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

hard_vote = load_solution(__file__).hard_vote
soft_vote = load_solution(__file__).soft_vote

def test_hard_vote_majority():
    preds = np.array([[0, 1, 2], [0, 1, 1], [1, 1, 1]])
    assert hard_vote(preds).tolist() == [0, 1, 1]


def test_hard_vote_tie_goes_to_smallest_label():
    preds = np.array([[2], [5]])
    assert hard_vote(preds).tolist() == [2]


def test_hard_vote_non_contiguous_labels():
    preds = np.array([[7, 9], [7, 9], [3, 9]])
    assert hard_vote(preds).tolist() == [7, 9]


def test_soft_vote_averages_probabilities():
    probs = np.array([[[0.9, 0.1]], [[0.8, 0.2]], [[0.2, 0.8]]])
    assert soft_vote(probs).tolist() == [0]


def test_hard_and_soft_can_disagree():
    # Two lukewarm votes for class 0, one very confident vote for class 1.
    probs = np.array([[[0.51, 0.49]], [[0.51, 0.49]], [[0.0, 1.0]]])
    preds = np.argmax(probs, axis=2)
    assert hard_vote(preds).tolist() == [0]
    assert soft_vote(probs).tolist() == [1]


def test_soft_vote_weights_change_the_winner():
    probs = np.array([[[0.9, 0.1]], [[0.2, 0.8]]])
    assert soft_vote(probs, weights=[1.0, 1.0]).tolist() == [0]
    assert soft_vote(probs, weights=[1.0, 5.0]).tolist() == [1]


def test_soft_vote_tie_goes_to_smallest_index():
    probs = np.array([[[0.5, 0.5]]])
    assert soft_vote(probs).tolist() == [0]


def test_single_model_reduces_to_argmax():
    rng = np.random.default_rng(0)
    probs = rng.dirichlet(np.ones(4), size=(1, 20))
    assert soft_vote(probs).tolist() == np.argmax(probs[0], axis=1).tolist()


def test_output_length_matches_samples():
    assert hard_vote(np.zeros((3, 7), dtype=int)).shape == (7,)
    assert soft_vote(np.full((3, 7, 2), 0.5)).shape == (7,)
