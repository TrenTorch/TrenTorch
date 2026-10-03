"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
seeded_kmeans = _module.seeded_kmeans

X_BLOBS = np.array([[0.0, 0.0], [0.1, 0.0], [10.0, 10.0], [10.1, 10.0]])
SEEDS_ONE_PER_CLASS = np.array([0, -1, 1, -1])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_two_blobs_are_recovered_from_one_seed_each():
    labels, _ = seeded_kmeans(X_BLOBS, SEEDS_ONE_PER_CLASS, 2)
    assert labels.tolist() == [0, 0, 1, 1]


def test_centroids_are_means_of_final_clusters():
    labels, centroids = seeded_kmeans(X_BLOBS, SEEDS_ONE_PER_CLASS, 2)
    assert np.allclose(centroids[0], [0.05, 0.0])
    assert np.allclose(centroids[1], [10.05, 10.0])


def test_seeded_points_keep_their_label():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(30, 2))
    seeds = -np.ones(30, dtype=int)
    seeds[:3] = 0
    seeds[3:6] = 1
    labels, _ = seeded_kmeans(X, seeds, 2)
    assert np.array_equal(labels[seeds >= 0], seeds[seeds >= 0])


def test_labels_have_expected_shape_and_range():
    labels, centroids = seeded_kmeans(X_BLOBS, SEEDS_ONE_PER_CLASS, 2)
    assert labels.shape == (4,) and centroids.shape == (2, 2)
    assert set(labels.tolist()) <= {0, 1}


def test_seed_is_not_moved_even_when_another_centroid_is_nearer():
    # Seed for class 0 sits at x = 9 while class 1's seed sits at x = 10.
    # The unlabeled point at x = 9.6 is nearer class 1's seed, but no seed moves.
    X = np.array([[9.0], [10.0], [9.6]])
    seeds = np.array([0, 1, -1])
    labels, _ = seeded_kmeans(X, seeds, 2)
    assert labels[0] == 0 and labels[1] == 1


def test_unlabeled_point_joins_nearest_centroid():
    X = np.array([[0.0], [10.0], [1.0], [9.0]])
    seeds = np.array([0, 1, -1, -1])
    labels, _ = seeded_kmeans(X, seeds, 2)
    assert labels.tolist() == [0, 1, 0, 1]


def test_three_classes_with_one_seed_each():
    X = np.array([[0.0, 0.0], [0.2, 0.0], [5.0, 0.0], [5.2, 0.0], [0.0, 5.0], [0.2, 5.0]])
    seeds = np.array([0, -1, 1, -1, 2, -1])
    labels, _ = seeded_kmeans(X, seeds, 3)
    assert labels.tolist() == [0, 0, 1, 1, 2, 2]


def test_converges_before_iteration_limit_on_clean_data():
    labels_short, _ = seeded_kmeans(X_BLOBS, SEEDS_ONE_PER_CLASS, 2, iters=2)
    labels_long, _ = seeded_kmeans(X_BLOBS, SEEDS_ONE_PER_CLASS, 2, iters=200)
    assert np.array_equal(labels_short, labels_long)


def test_class_without_a_seed_raises():
    assert _raises_value_error(seeded_kmeans, X_BLOBS, np.array([0, 0, -1, -1]), 2)


def test_seed_out_of_range_raises():
    assert _raises_value_error(seeded_kmeans, X_BLOBS, np.array([0, 2, -1, -1]), 2)


def test_shape_mismatch_raises():
    assert _raises_value_error(seeded_kmeans, X_BLOBS, np.array([0, 1]), 2)


def test_zero_iterations_raises():
    assert _raises_value_error(seeded_kmeans, X_BLOBS, SEEDS_ONE_PER_CLASS, 2, 0)


def test_inputs_are_not_modified():
    X = X_BLOBS.copy()
    seeds = SEEDS_ONE_PER_CLASS.copy()
    seeded_kmeans(X, seeds, 2)
    assert np.array_equal(X, X_BLOBS) and np.array_equal(seeds, SEEDS_ONE_PER_CLASS)
