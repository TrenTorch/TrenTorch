"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

kmeans_assign = load_solution(__file__).kmeans_assign


def test_matches_hand_computation():
    input = np.array([[0.0], [1.0], [9.0], [10.0]])
    centroids = np.array([[0.5], [9.5]])
    result = kmeans_assign(input, centroids)
    assert np.array_equal(result, [0, 0, 1, 1])


def test_returns_one_index_per_sample():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(30, 2))
    centroids = rng.normal(size=(4, 2))
    result = kmeans_assign(input, centroids)
    assert result.shape == (30,)
    assert result.min() >= 0
    assert result.max() < 4


def test_ties_break_to_the_lower_centroid_index():
    input = np.array([[0.5]])
    centroids = np.array([[0.0], [1.0]])  # both exactly 0.5 away
    result = kmeans_assign(input, centroids)
    assert result[0] == 0


def test_single_centroid_assigns_everything_to_it():
    input = np.array([[1.0], [-5.0], [100.0]])
    centroids = np.array([[0.0]])
    result = kmeans_assign(input, centroids)
    assert np.array_equal(result, [0, 0, 0])


def test_matches_manual_nearest_centroid_across_random_configs():
    rng = np.random.default_rng(1)
    for seed in range(5):
        rng2 = np.random.default_rng(seed)
        input = rng2.normal(size=(25, 3))
        centroids = rng2.normal(size=(5, 3))
        result = kmeans_assign(input, centroids)
        for i, point in enumerate(input):
            manual_distances = np.sqrt(np.sum((centroids - point) ** 2, axis=1))
            assert result[i] == np.argmin(manual_distances)
