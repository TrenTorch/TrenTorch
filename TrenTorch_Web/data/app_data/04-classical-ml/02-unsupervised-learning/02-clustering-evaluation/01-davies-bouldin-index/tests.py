"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

davies_bouldin_index = load_solution(__file__).davies_bouldin_index


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


# two clusters, centroids (0, 1) and (10, 1), scatter 1 each, separation 10
X_TWO = np.array([[0.0, 0.0], [0.0, 2.0], [10.0, 0.0], [10.0, 2.0]])
LABELS_TWO = np.array([0, 0, 1, 1])


def test_worked_example_gives_point_two():
    # R = (1 + 1) / 10 for each cluster
    assert np.isclose(davies_bouldin_index(X_TWO, LABELS_TWO), 0.2)


def test_well_separated_tight_clusters_score_near_zero():
    rng = np.random.default_rng(0)
    a = rng.normal(0.0, 0.01, size=(20, 2))
    b = rng.normal(100.0, 0.01, size=(20, 2))
    X = np.vstack([a, b])
    labels = np.array([0] * 20 + [1] * 20)
    assert davies_bouldin_index(X, labels) < 0.01


def test_overlapping_clusters_score_higher_than_separated_ones():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(60, 2))
    labels = np.array([0] * 30 + [1] * 30)
    shifted = X.copy()
    shifted[30:] += 50.0
    assert davies_bouldin_index(shifted, labels) < davies_bouldin_index(X, labels)


def test_scale_invariant_in_the_ratio():
    # multiplying all coordinates by a constant scales both scatter and distance equally
    assert np.isclose(davies_bouldin_index(X_TWO, LABELS_TWO), davies_bouldin_index(3.0 * X_TWO, LABELS_TWO))


def test_translation_invariant():
    assert np.isclose(davies_bouldin_index(X_TWO, LABELS_TWO), davies_bouldin_index(X_TWO + 42.0, LABELS_TWO))


def test_is_non_negative():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(40, 3))
    labels = rng.integers(0, 4, size=40)
    labels[:4] = [0, 1, 2, 3]
    assert davies_bouldin_index(X, labels) >= 0.0


def test_label_renaming_does_not_change_the_index():
    renamed = np.array([7, 7, 3, 3])
    assert np.isclose(davies_bouldin_index(X_TWO, LABELS_TWO), davies_bouldin_index(X_TWO, renamed))


def test_three_clusters_average_their_worst_neighbors():
    X = np.array([[0.0, 0.0], [0.0, 2.0], [10.0, 0.0], [10.0, 2.0], [0.0, 20.0], [0.0, 22.0]])
    labels = np.array([0, 0, 1, 1, 2, 2])
    # every cluster has scatter 1. Centroids: (0,1), (10,1), (0,21).
    # cluster 0 worst is 2/10 (against cluster 1); cluster 1 worst is 2/10 (against cluster 0);
    # cluster 2 worst is 2/20 (against cluster 0, the nearer of its two neighbors)
    expected = (2 / 10 + 2 / 10 + 2 / 20) / 3
    assert np.isclose(davies_bouldin_index(X, labels), expected)


def test_fewer_than_two_clusters_raises():
    assert _raises_value_error(davies_bouldin_index, X_TWO, np.array([0, 0, 0, 0]))


def test_identical_centroids_do_not_crash_silently():
    X = np.array([[-1.0, 0.0], [1.0, 0.0], [-1.0, 0.0], [1.0, 0.0]])
    labels = np.array([0, 0, 1, 1])
    with np.errstate(divide="ignore", invalid="ignore"):
        value = davies_bouldin_index(X, labels)
    assert np.isinf(value) or np.isnan(value) or value > 0


def test_returns_a_python_float():
    assert isinstance(davies_bouldin_index(X_TWO, LABELS_TWO), float)


def test_does_not_modify_inputs():
    X = X_TWO.copy()
    labels = LABELS_TWO.copy()
    davies_bouldin_index(X, labels)
    assert np.array_equal(X, X_TWO)
    assert np.array_equal(labels, LABELS_TWO)
