"""
pytest data/app_data/01-classical-ml/06-unsupervised/02-kmeans-centroid-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

kmeans_update_centroids = load_solution(
    f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}"
).kmeans_update_centroids


def test_matches_hand_computation():
    input = np.array([[0.0], [2.0], [10.0], [12.0]])
    assignments = np.array([0, 0, 1, 1])
    centroids = np.array([[100.0], [100.0]])  # deliberately wrong, should be overwritten
    result = kmeans_update_centroids(input, assignments, centroids)
    assert np.allclose(result, [[1.0], [11.0]])


def test_empty_cluster_keeps_its_old_centroid():
    input = np.array([[0.0], [1.0], [2.0]])
    assignments = np.array([0, 0, 0])  # nothing assigned to cluster 1
    centroids = np.array([[50.0], [999.0]])
    result = kmeans_update_centroids(input, assignments, centroids)
    assert np.isclose(result[1, 0], 999.0)
    assert np.isclose(result[0, 0], 1.0)


def test_does_not_mutate_the_original_centroids_array():
    input = np.array([[5.0], [7.0]])
    assignments = np.array([0, 0])
    centroids = np.array([[0.0]])
    original = centroids.copy()
    kmeans_update_centroids(input, assignments, centroids)
    assert np.array_equal(centroids, original)


def test_multi_feature_update_matches_hand_computation():
    input = np.array([[0.0, 0.0], [2.0, 4.0], [10.0, 0.0]])
    assignments = np.array([0, 0, 1])
    centroids = np.zeros((2, 2))
    result = kmeans_update_centroids(input, assignments, centroids)
    assert np.allclose(result[0], [1.0, 2.0])
    assert np.allclose(result[1], [10.0, 0.0])


def test_one_full_iteration_moves_centroids_toward_true_cluster_centers():
    rng = np.random.default_rng(0)
    true_centers = np.array([[-5.0, -5.0], [5.0, 5.0]])
    input = np.vstack([true_centers[0] + rng.normal(scale=0.5, size=(30, 2)),
                        true_centers[1] + rng.normal(scale=0.5, size=(30, 2))])
    bad_start = np.array([[-4.0, -6.0], [6.0, 4.0]])

    load_kmeans_assign = load_solution(
        "01-classical-ml/06-unsupervised/01-kmeans-assignment"
    ).kmeans_assign
    assignments = load_kmeans_assign(input, bad_start)
    updated = kmeans_update_centroids(input, assignments, bad_start)

    dist_before = np.sum((bad_start - true_centers) ** 2)
    dist_after = np.sum((updated - true_centers) ** 2)
    assert dist_after < dist_before
