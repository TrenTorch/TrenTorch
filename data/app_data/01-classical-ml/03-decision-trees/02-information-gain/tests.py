"""
pytest data/app_data/01-classical-ml/03-decision-trees/02-information-gain/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

information_gain = load_solution(
    f"01-classical-ml/03-decision-trees/{Path(__file__).resolve().parent.name}"
).information_gain
gini_impurity = load_solution("01-classical-ml/03-decision-trees/01-gini-impurity").gini_impurity


def test_perfect_split_matches_hand_computation():
    # parent=[0,0,1,1], gini=0.5. Both children pure -> gini=0 each.
    # gain = 0.5 - 0 = 0.5, the maximum possible gain for this parent.
    parent = np.array([0, 0, 1, 1])
    left = np.array([0, 0])
    right = np.array([1, 1])
    assert np.isclose(information_gain(parent, left, right), 0.5)


def test_useless_split_gives_zero_gain():
    # Splitting off nothing (everything in left, right empty) can't
    # reduce impurity at all -- gain must be exactly 0.
    parent = np.array([0, 0, 1, 1, 1])
    left = parent.copy()
    right = np.array([], dtype=int)
    assert np.isclose(information_gain(parent, left, right), 0.0)


def test_imbalanced_but_pure_children_matches_hand_computation():
    # parent=[0]*6+[1]*2, gini=0.375. Both children pure (each all one
    # class), regardless of how unevenly sized -- weighted child
    # impurity is 0, so gain = 0.375 exactly.
    parent = np.array([0, 0, 0, 0, 0, 0, 1, 1])
    left = np.array([0, 0, 0, 0, 0, 0])
    right = np.array([1, 1])
    assert np.isclose(information_gain(parent, left, right), 0.375)


def test_children_weighted_by_size_not_averaged_evenly():
    # Directly targets the "used 0.5/0.5 instead of size-proportional
    # weights" mutant: with unequal, non-pure child sizes, weighting by
    # size vs. plain averaging give numerically different (and here,
    # different-signed) results.
    parent = np.array([0, 0, 0, 0, 0, 1, 0, 1])  # 6 zeros, 2 ones
    left = np.array([0, 0, 0, 0, 0, 1])  # size 6
    right = np.array([0, 1])  # size 2
    assert np.isclose(information_gain(parent, left, right), 0.041666666, atol=1e-6)


def test_single_class_parent_gives_zero_gain_for_any_split():
    # A pure parent has nothing to gain -- both children of a pure
    # parent are necessarily pure too, gain is exactly 0.
    parent = np.array([1, 1, 1, 1])
    left = np.array([1, 1])
    right = np.array([1, 1])
    assert np.isclose(information_gain(parent, left, right), 0.0)


def test_gain_is_never_negative():
    # Real mathematical property of Gini impurity: splitting a node can
    # only maintain or reduce total impurity, never increase it. Any
    # correct implementation must respect this across arbitrary splits,
    # not just the hand-picked cases above.
    rng = np.random.default_rng(0)
    for _ in range(20):
        n = rng.integers(4, 50)
        n_classes = rng.integers(2, 5)
        parent = rng.integers(0, n_classes, size=n)
        split_point = rng.integers(1, n)
        order = rng.permutation(n)
        left = parent[order[:split_point]]
        right = parent[order[split_point:]]
        gain = information_gain(parent, left, right)
        assert gain >= -1e-9, f"negative gain: {gain}"


def test_matches_independent_recomputation_from_class_counts():
    # An oracle built directly from class-count fractions, not by
    # calling gini_impurity a second time -- exercises the same formula
    # through a different code path.
    rng = np.random.default_rng(1)
    for _ in range(10):
        n = rng.integers(6, 40)
        parent = rng.integers(0, 3, size=n)
        split_point = rng.integers(1, n)
        left, right = parent[:split_point], parent[split_point:]

        def gini_from_counts(labels):
            if labels.size == 0:
                return 0.0
            _, counts = np.unique(labels, return_counts=True)
            p = counts / labels.size
            return 1.0 - (p**2).sum()

        expected = gini_from_counts(parent) - (
            (left.size / n) * gini_from_counts(left) + (right.size / n) * gini_from_counts(right)
        )
        assert np.isclose(information_gain(parent, left, right), expected, atol=1e-9)
