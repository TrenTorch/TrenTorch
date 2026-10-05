"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

k_medoids = load_solution(__file__).k_medoids


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def _two_blobs():
    rng = np.random.default_rng(0)
    a = rng.normal(0.0, 0.1, size=(12, 2))
    b = rng.normal(50.0, 0.1, size=(12, 2))
    return np.vstack([a, b])


def test_separates_two_well_separated_blobs():
    labels, _ = k_medoids(_two_blobs(), 2, seed=1)
    assert len(set(labels[:12])) == 1
    assert len(set(labels[12:])) == 1
    assert labels[0] != labels[12]


def test_medoids_are_actual_row_indices_one_per_cluster():
    X = _two_blobs()
    labels, medoids = k_medoids(X, 2, seed=2)
    assert len(medoids) == 2
    assert len(set(medoids.tolist())) == 2
    assert np.all((medoids >= 0) & (medoids < len(X)))


def test_each_medoid_belongs_to_its_own_cluster():
    X = _two_blobs()
    labels, medoids = k_medoids(X, 2, seed=3)
    for c, m in enumerate(medoids):
        assert labels[m] == c


def test_labels_are_in_range_and_one_per_point():
    X = _two_blobs()
    labels, _ = k_medoids(X, 3, seed=4)
    assert labels.shape == (len(X),)
    assert set(labels.tolist()).issubset({0, 1, 2})


def test_single_cluster_medoid_is_the_most_central_point():
    X = np.array([[0.0], [1.0], [10.0]])
    labels, medoids = k_medoids(X, 1, seed=0)
    # distance sums: from 0 -> 11, from 1 -> 10, from 10 -> 19
    assert medoids.tolist() == [1]
    assert np.all(labels == 0)


def test_medoid_is_robust_to_an_outlier():
    X = np.array([[0.0], [0.1], [0.2], [0.3], [1000.0]])
    _, medoids = k_medoids(X, 1, seed=5)
    assert X[medoids[0], 0] < 1.0


def test_same_seed_gives_the_same_result():
    X = _two_blobs()
    a_labels, a_medoids = k_medoids(X, 2, seed=6)
    b_labels, b_medoids = k_medoids(X, 2, seed=6)
    assert np.array_equal(a_labels, b_labels)
    assert np.array_equal(a_medoids, b_medoids)


def test_k_equal_to_n_makes_every_point_a_medoid():
    X = np.array([[0.0], [5.0], [9.0]])
    labels, medoids = k_medoids(X, 3, seed=0)
    assert sorted(medoids.tolist()) == [0, 1, 2]
    assert sorted(labels.tolist()) == [0, 1, 2]


def test_k_below_one_raises():
    assert _raises_value_error(k_medoids, _two_blobs(), 0)


def test_k_above_n_raises():
    assert _raises_value_error(k_medoids, np.zeros((2, 2)), 3)


def test_returns_integer_medoid_indices():
    _, medoids = k_medoids(_two_blobs(), 2, seed=7)
    assert np.issubdtype(medoids.dtype, np.integer)


def test_does_not_modify_the_data():
    X = _two_blobs()
    before = X.copy()
    k_medoids(X, 2, seed=8)
    assert np.array_equal(X, before)


def test_converges_to_the_same_partition_from_different_starts():
    X = _two_blobs()
    a, _ = k_medoids(X, 2, seed=10)
    b, _ = k_medoids(X, 2, seed=11)
    assert np.array_equal(a, b) or np.array_equal(a, 1 - b)
