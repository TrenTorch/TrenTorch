"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

birch_subclusters = load_solution(__file__).birch_subclusters


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _two_groups():
    a = np.array([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1]])
    b = np.array([[5.0, 5.0], [5.1, 5.0], [5.0, 5.1]])
    return np.vstack([a, b])


def test_nearby_points_merge_and_far_groups_split():
    labels, _ = birch_subclusters(_two_groups(), 0.5)
    assert len(np.unique(labels)) == 2
    assert len(set(labels[:3])) == 1
    assert len(set(labels[3:])) == 1


def test_zero_threshold_keeps_distinct_points_apart():
    X = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]])
    labels, centroids = birch_subclusters(X, 0.0)
    assert len(np.unique(labels)) == 3
    assert centroids.shape == (3, 2)


def test_huge_threshold_merges_everything():
    labels, centroids = birch_subclusters(_two_groups(), 1000.0)
    assert np.all(labels == 0)
    assert centroids.shape == (1, 2)


def test_centroids_are_means_of_their_members():
    X = _two_groups()
    labels, centroids = birch_subclusters(X, 0.5)
    for k in range(len(centroids)):
        assert np.allclose(centroids[k], X[labels == k].mean(axis=0))


def test_every_subcluster_radius_is_within_threshold():
    X = _two_groups()
    threshold = 0.5
    labels, centroids = birch_subclusters(X, threshold)
    for k in range(len(centroids)):
        members = X[labels == k]
        radius = np.sqrt(np.mean(np.sum((members - centroids[k]) ** 2, axis=1)))
        assert radius <= threshold + 1e-9


def test_labels_are_consecutive_from_zero():
    labels, centroids = birch_subclusters(_two_groups(), 0.5)
    assert sorted(np.unique(labels).tolist()) == list(range(len(centroids)))


def test_one_label_per_row_and_integer_dtype():
    X = _two_groups()
    labels, _ = birch_subclusters(X, 0.5)
    assert labels.shape == (len(X),)
    assert np.issubdtype(labels.dtype, np.integer)


def test_single_point_forms_one_subcluster():
    labels, centroids = birch_subclusters(np.array([[3.0, 4.0]]), 0.1)
    assert labels.tolist() == [0]
    assert np.allclose(centroids, [[3.0, 4.0]])


def test_negative_threshold_raises():
    assert _raises_value_error(birch_subclusters, _two_groups(), -0.1)


def test_same_input_gives_same_summary():
    X = _two_groups()
    l1, c1 = birch_subclusters(X, 0.5)
    l2, c2 = birch_subclusters(X, 0.5)
    assert np.array_equal(l1, l2)
    assert np.array_equal(c1, c2)


def test_does_not_modify_the_data():
    X = _two_groups()
    before = X.copy()
    birch_subclusters(X, 0.5)
    assert np.array_equal(X, before)
