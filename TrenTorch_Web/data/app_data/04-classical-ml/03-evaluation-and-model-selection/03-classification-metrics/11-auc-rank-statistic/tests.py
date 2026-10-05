"""
pytest tests.py
"""

import itertools

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
auc_rank = _module.auc_rank


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _pairwise_auc(scores, labels):
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    total = 0.0
    for p, n in itertools.product(pos, neg):
        total += 1.0 if p > n else (0.5 if p == n else 0.0)
    return total / (len(pos) * len(neg))


def test_perfect_separation_gives_one():
    assert np.isclose(auc_rank(np.array([0.1, 0.2, 0.8, 0.9]), np.array([0, 0, 1, 1])), 1.0)


def test_reversed_separation_gives_zero():
    assert np.isclose(auc_rank(np.array([0.9, 0.8, 0.2, 0.1]), np.array([0, 0, 1, 1])), 0.0)


def test_all_tied_scores_give_one_half():
    assert np.isclose(auc_rank(np.ones(6), np.array([0, 1, 0, 1, 0, 1])), 0.5)


def test_hand_example_gives_three_quarters():
    scores = np.array([0.1, 0.4, 0.35, 0.8])
    labels = np.array([0, 0, 1, 1])
    assert np.isclose(auc_rank(scores, labels), 0.75)


def test_matches_pairwise_definition_on_random_scores():
    rng = np.random.default_rng(0)
    scores = rng.random(30)
    labels = rng.integers(0, 2, size=30)
    if labels.sum() == 0 or labels.sum() == 30:
        labels[0], labels[1] = 0, 1
    assert np.isclose(auc_rank(scores, labels), _pairwise_auc(scores, labels))


def test_matches_pairwise_definition_with_ties():
    scores = np.array([0.5, 0.5, 0.2, 0.9, 0.5])
    labels = np.array([1, 0, 0, 1, 1])
    assert np.isclose(auc_rank(scores, labels), _pairwise_auc(scores, labels))


def test_invariant_to_monotone_transform():
    rng = np.random.default_rng(1)
    scores = rng.random(20)
    labels = rng.integers(0, 2, size=20)
    labels[0], labels[1] = 0, 1
    assert np.isclose(auc_rank(scores, labels), auc_rank(np.exp(5 * scores), labels))


def test_flipping_labels_gives_one_minus_auc():
    rng = np.random.default_rng(2)
    scores = rng.random(15)
    labels = rng.integers(0, 2, size=15)
    labels[0], labels[1] = 0, 1
    assert np.isclose(auc_rank(scores, 1 - labels), 1 - auc_rank(scores, labels))


def test_result_is_between_zero_and_one():
    rng = np.random.default_rng(3)
    scores = rng.random(12)
    labels = np.array([0, 1] * 6)
    assert 0.0 <= auc_rank(scores, labels) <= 1.0


def test_single_positive_is_ranked_correctly():
    # Positive scores 0.7; negatives 0.1 and 0.9. Pairs won: one of two, so AUC = 0.5.
    assert np.isclose(auc_rank(np.array([0.1, 0.7, 0.9]), np.array([0, 1, 0])), 0.5)


def test_only_one_class_raises():
    assert _raises_value_error(auc_rank, np.array([0.1, 0.2]), np.array([1, 1]))


def test_non_binary_label_raises():
    assert _raises_value_error(auc_rank, np.array([0.1, 0.2]), np.array([0, 2]))


def test_length_mismatch_raises():
    assert _raises_value_error(auc_rank, np.array([0.1, 0.2, 0.3]), np.array([0, 1]))


def test_inputs_are_not_modified():
    scores = np.array([0.4, 0.4, 0.1])
    labels = np.array([1, 0, 0])
    s0, y0 = scores.copy(), labels.copy()
    auc_rank(scores, labels)
    assert np.array_equal(scores, s0) and np.array_equal(labels, y0)
