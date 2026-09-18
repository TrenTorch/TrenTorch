"""
pytest data/app_data/01-classical-ml/05-instance-based-probabilistic/01-knn/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/05-instance-based-probabilistic/{Path(__file__).resolve().parent.name}"
)
pairwise_distances = _module.pairwise_distances
knn_predict = _module.knn_predict


def test_pairwise_distances_matches_hand_computation():
    input = np.array([[0.0, 0.0], [3.0, 4.0]])
    queries = np.array([[0.0, 0.0]])
    # distance to (0,0) is 0, distance to (3,4) is the classic 3-4-5 triangle: 5
    result = pairwise_distances(input, queries)
    assert result.shape == (1, 2)
    assert np.allclose(result, [[0.0, 5.0]])


def test_pairwise_distances_is_symmetric_between_identical_points():
    points = np.array([[1.0, 2.0], [3.0, -1.0], [0.0, 0.0]])
    result = pairwise_distances(points, points)
    assert np.allclose(np.diag(result), 0.0)


def test_knn_predict_k1_matches_the_single_nearest_neighbor():
    input = np.array([[0.0], [10.0], [20.0]])
    labels = np.array([0, 1, 2])
    queries = np.array([[0.5], [19.0]])
    result = knn_predict(input, labels, queries, k=1)
    assert np.array_equal(result, [0, 2])


def test_knn_predict_majority_vote_among_k_neighbors():
    # Query at 5, with points at 0,4,6,10,20 (labels 0,0,1,1,1). Nearest
    # 3 are 4,6,0 (distances 1,1,5) -> labels 0,1,0 -> majority 0.
    input = np.array([[0.0], [4.0], [6.0], [10.0], [20.0]])
    labels = np.array([0, 0, 1, 1, 1])
    queries = np.array([[5.0]])
    result = knn_predict(input, labels, queries, k=3)
    assert result[0] == 0


def test_knn_predict_ties_break_to_lower_class_label():
    input = np.array([[0.0], [1.0]])
    labels = np.array([5, 2])
    queries = np.array([[0.5]])  # exactly equidistant from both
    result = knn_predict(input, labels, queries, k=2)
    assert result[0] == 2


def test_knn_predict_handles_multiple_queries_independently():
    input = np.array([[-10.0], [-9.0], [9.0], [10.0]])
    labels = np.array([0, 0, 1, 1])
    queries = np.array([[-9.5], [9.5], [0.0]])
    result = knn_predict(input, labels, queries, k=1)
    assert result[0] == 0
    assert result[1] == 1


def test_larger_k_can_change_the_prediction():
    # 1 nearby point of class 1, several farther points of class 0 --
    # k=1 should follow the nearest point, a larger k should out-vote it.
    input = np.array([[0.1], [5.0], [5.1], [5.2], [5.3]])
    labels = np.array([1, 0, 0, 0, 0])
    queries = np.array([[0.0]])
    assert knn_predict(input, labels, queries, k=1)[0] == 1
    assert knn_predict(input, labels, queries, k=5)[0] == 0


def test_matches_manual_brute_force_across_random_configs():
    rng = np.random.default_rng(0)
    for seed in range(5):
        rng2 = np.random.default_rng(seed)
        input = rng2.normal(size=(30, 3))
        labels = rng2.integers(0, 3, 30)
        queries = rng2.normal(size=(5, 3))
        k = 4
        result = knn_predict(input, labels, queries, k)
        for i, query in enumerate(queries):
            manual_distances = np.sqrt(np.sum((input - query) ** 2, axis=1))
            manual_nearest = np.argsort(manual_distances)[:k]
            manual_labels = labels[manual_nearest]
            values, counts = np.unique(manual_labels, return_counts=True)
            expected = values[np.argmax(counts)]
            assert result[i] == expected
