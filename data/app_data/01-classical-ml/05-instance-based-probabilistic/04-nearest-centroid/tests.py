"""
pytest data/app_data/01-classical-ml/05-instance-based-probabilistic/04-nearest-centroid/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/05-instance-based-probabilistic/{Path(__file__).resolve().parent.name}"
)
nearest_centroid_fit = _module.nearest_centroid_fit
nearest_centroid_predict = _module.nearest_centroid_predict


def test_centroids_match_hand_computed_means():
    input = np.array([[0.0, 0.0], [2.0, 0.0], [10.0, 10.0], [12.0, 10.0]])
    labels = np.array([0, 0, 1, 1])
    model = nearest_centroid_fit(input, labels)
    assert np.allclose(model["centroids"][0], [1.0, 0.0])
    assert np.allclose(model["centroids"][1], [11.0, 10.0])


def test_predict_matches_hand_computation():
    input = np.array([[0.0], [2.0], [10.0], [12.0]])
    labels = np.array([0, 0, 1, 1])
    model = nearest_centroid_fit(input, labels)
    queries = np.array([[0.5], [11.0]])
    predictions = nearest_centroid_predict(model, queries)
    assert np.array_equal(predictions, [0, 1])


def test_equidistant_query_breaks_to_the_lower_class_label():
    input = np.array([[0.0], [2.0], [10.0], [12.0]])
    labels = np.array([0, 0, 1, 1])
    model = nearest_centroid_fit(input, labels)
    # centroids are 1.0 and 11.0 -- exact midpoint 6.0 is equidistant
    predictions = nearest_centroid_predict(model, np.array([[6.0]]))
    assert predictions[0] == 0


def test_separates_clearly_clustered_classes():
    rng = np.random.default_rng(2)
    class0 = rng.normal(loc=-3.0, size=(20, 2))
    class1 = rng.normal(loc=3.0, size=(20, 2))
    input = np.vstack([class0, class1])
    labels = np.concatenate([np.zeros(20, dtype=int), np.ones(20, dtype=int)])
    model = nearest_centroid_fit(input, labels)
    predictions = nearest_centroid_predict(model, input)
    assert np.mean(predictions == labels) > 0.95


def test_uses_mean_not_median_or_first_point():
    # Directly targets a mutant that returns the first row of a class
    # (or its median) instead of its actual mean -- an outlier shifts
    # the mean noticeably but wouldn't budge a median or a "first row".
    input = np.array([[0.0], [0.0], [0.0], [30.0]])  # heavily skewed by one outlier
    labels = np.array([0, 0, 0, 0])
    model = nearest_centroid_fit(input, labels)
    assert np.isclose(model["centroids"][0][0], 7.5)  # mean of 0,0,0,30


def test_matches_manual_nearest_centroid_across_random_configs():
    rng = np.random.default_rng(9)
    for seed in range(5):
        rng2 = np.random.default_rng(seed)
        input = rng2.normal(size=(40, 3))
        labels = rng2.integers(0, 3, 40)
        queries = rng2.normal(size=(6, 3))

        predictions = nearest_centroid_predict(nearest_centroid_fit(input, labels), queries)

        classes = np.unique(labels)
        manual_centroids = np.array([input[labels == c].mean(axis=0) for c in classes])
        for i, query in enumerate(queries):
            manual_distances = np.sqrt(np.sum((manual_centroids - query) ** 2, axis=1))
            expected = classes[np.argmin(manual_distances)]
            assert predictions[i] == expected
