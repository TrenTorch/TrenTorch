"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

silhouette_score = load_solution(__file__).silhouette_score


def _oracle(X, labels):
    n = len(X)
    total = 0.0
    for i in range(n):
        own = [j for j in range(n) if labels[j] == labels[i] and j != i]
        if not own:
            continue
        a = sum(math.dist(X[i], X[j]) for j in own) / len(own)
        b = math.inf
        for c in set(labels):
            if c == labels[i]:
                continue
            members = [j for j in range(n) if labels[j] == c]
            b = min(b, sum(math.dist(X[i], X[j]) for j in members) / len(members))
        total += (b - a) / max(a, b)
    return total / n


def test_hand_computed_1d_example():
    X = np.array([[0.0], [1.0], [10.0], [11.0]])
    labels = np.array([0, 0, 1, 1])
    # Point 0: a = 1, b = mean(10, 11) = 10.5. Point 1: a = 1, b = mean(9, 10) = 9.5.
    # The other cluster mirrors this.
    assert np.isclose(silhouette_score(X, labels), (9.5 / 10.5 + 8.5 / 9.5) / 2)


def test_well_separated_clusters_score_near_one():
    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal(0, 0.1, (20, 2)), rng.normal(50, 0.1, (20, 2))])
    labels = np.array([0] * 20 + [1] * 20)
    assert silhouette_score(X, labels) > 0.99


def test_bad_assignment_scores_lower():
    rng = np.random.default_rng(1)
    X = np.vstack([rng.normal(0, 0.5, (15, 2)), rng.normal(8, 0.5, (15, 2))])
    good = np.array([0] * 15 + [1] * 15)
    bad = np.array([0, 1] * 15)
    assert silhouette_score(X, good) > silhouette_score(X, bad)


def test_single_cluster_is_zero():
    assert silhouette_score(np.array([[0.0], [1.0], [2.0]]), np.array([5, 5, 5])) == 0.0


def test_singleton_cluster_contributes_zero():
    X = np.array([[0.0], [1.0], [100.0]])
    labels = np.array([0, 0, 1])
    # Point 0: a = 1, b = 100. Point 1: a = 1, b = 99. The singleton has s = 0.
    expected = ((100 - 1) / 100 + (99 - 1) / 99 + 0.0) / 3
    assert np.isclose(silhouette_score(X, labels), expected)


def test_matches_independent_oracle():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(25, 3))
    labels = rng.integers(0, 3, size=25)
    assert np.isclose(silhouette_score(X, labels), _oracle(X.tolist(), labels.tolist()))


def test_label_values_do_not_matter():
    rng = np.random.default_rng(5)
    X = rng.normal(size=(20, 2))
    labels = rng.integers(0, 2, size=20)
    assert np.isclose(silhouette_score(X, labels), silhouette_score(X, labels * 7 + 3))


def test_score_is_within_bounds():
    rng = np.random.default_rng(6)
    value = silhouette_score(rng.normal(size=(30, 2)), rng.integers(0, 4, size=30))
    assert -1.0 <= value <= 1.0


def test_returns_python_float():
    assert isinstance(silhouette_score(np.array([[0.0], [1.0]]), np.array([0, 1])), float)
