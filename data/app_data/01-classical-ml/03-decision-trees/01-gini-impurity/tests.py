"""
pytest data/app_data/01-classical-ml/03-decision-trees/01-gini-impurity/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gini_impurity = load_solution(
    f"01-classical-ml/03-decision-trees/{Path(__file__).resolve().parent.name}"
).gini_impurity


def test_pure_node_is_zero():
    assert gini_impurity(np.array([1, 1, 1, 1])) == 0.0


def test_balanced_binary_is_one_half():
    assert np.isclose(gini_impurity(np.array([0, 0, 1, 1])), 0.5)


def test_balanced_three_classes_is_two_thirds():
    labels = np.array([0, 1, 2] * 4)
    assert np.isclose(gini_impurity(labels), 2.0 / 3.0)


def test_imbalanced_binary_matches_hand_computation():
    # p=[0.9, 0.1] -> 1 - (0.81 + 0.01) = 0.18. Also directly rules out
    # the "forgot the 1 -" mutant (sum(p**2)=0.82, clearly not 0.18) and
    # any denominator bug (dividing by class count instead of n_samples).
    labels = np.array([0] * 9 + [1])
    assert np.isclose(gini_impurity(labels), 0.18)


def test_non_contiguous_class_labels():
    # Labels aren't 0..k-1 -- np.unique must be doing the counting, not
    # an assumption that class indices are small contiguous integers.
    labels = np.array([5, 5, 7, 7, 7])
    assert np.isclose(gini_impurity(labels), 0.48)


def test_single_sample_is_pure():
    assert gini_impurity(np.array([42])) == 0.0


def test_empty_array_is_zero_by_convention():
    assert gini_impurity(np.array([], dtype=int)) == 0.0


def test_return_type_is_float():
    result = gini_impurity(np.array([0, 1, 1]))
    assert isinstance(result, float)


def test_matches_pairwise_disagreement_probability():
    # Independent oracle: Gini impurity also equals the probability two
    # independently-drawn samples from this node have *different*
    # labels, sum(2 * p_i * p_j for i < j). Computed here with an
    # explicit double loop over class pairs, not the closed-form
    # 1 - sum(p^2) the solution itself uses, across several random
    # label sets and class counts.
    rng = np.random.default_rng(0)
    for n_classes in (2, 3, 5):
        labels = rng.integers(0, n_classes, size=200)
        _, counts = np.unique(labels, return_counts=True)
        probabilities = counts / labels.size
        pairwise_disagreement = 0.0
        for i in range(len(probabilities)):
            for j in range(len(probabilities)):
                if i != j:
                    pairwise_disagreement += probabilities[i] * probabilities[j]
        assert np.isclose(gini_impurity(labels), pairwise_disagreement, atol=1e-9)


def test_more_classes_never_exceeds_theoretical_maximum():
    # Gini impurity for k equally-likely classes maxes out at 1 - 1/k --
    # a sanity bound that catches a formula that grows unboundedly wrong
    # (e.g. missing the square) rather than being caught by exact
    # equality alone.
    rng = np.random.default_rng(1)
    for n_classes in (2, 4, 10):
        labels = rng.integers(0, n_classes, size=500)
        assert gini_impurity(labels) < 1.0 - 1.0 / n_classes + 1e-6
