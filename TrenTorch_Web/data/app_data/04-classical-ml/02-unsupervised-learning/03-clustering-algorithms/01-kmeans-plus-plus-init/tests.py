"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

kmeans_plus_plus_init = load_solution(__file__).kmeans_plus_plus_init


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def _two_blobs():
    rng = np.random.default_rng(0)
    a = rng.normal(0.0, 0.05, size=(10, 2))
    b = rng.normal(1000.0, 0.05, size=(10, 2))
    return np.vstack([a, b])


def test_returns_k_rows_of_the_right_width():
    X = _two_blobs()
    centers = kmeans_plus_plus_init(X, 3, seed=1)
    assert centers.shape == (3, 2)


def test_every_center_is_a_row_of_the_data():
    X = _two_blobs()
    centers = kmeans_plus_plus_init(X, 4, seed=2)
    for c in centers:
        assert np.any(np.all(np.isclose(X, c), axis=1))


def test_same_seed_gives_the_same_centers():
    X = _two_blobs()
    assert np.array_equal(kmeans_plus_plus_init(X, 3, seed=5), kmeans_plus_plus_init(X, 3, seed=5))


def test_separated_blobs_get_one_center_in_each_for_k_two():
    X = _two_blobs()
    for seed in range(5):
        centers = kmeans_plus_plus_init(X, 2, seed=seed)
        assert np.linalg.norm(centers[0] - centers[1]) > 500.0


def test_k_one_returns_a_single_data_point():
    X = _two_blobs()
    centers = kmeans_plus_plus_init(X, 1, seed=3)
    assert centers.shape == (1, 2)
    assert np.any(np.all(np.isclose(X, centers[0]), axis=1))


def test_k_equal_to_n_picks_every_distinct_point_once():
    X = np.array([[0.0, 0.0], [1.0, 3.0], [4.0, 4.0], [9.0, 1.0]])
    centers = kmeans_plus_plus_init(X, 4, seed=7)
    assert {tuple(row) for row in centers} == {tuple(row) for row in X}


def test_identical_points_do_not_crash():
    X = np.ones((5, 2))
    centers = kmeans_plus_plus_init(X, 3, seed=0)
    assert centers.shape == (3, 2)
    assert np.all(centers == 1.0)


def test_k_below_one_raises():
    assert _raises_value_error(kmeans_plus_plus_init, _two_blobs(), 0, 0)


def test_k_above_n_raises():
    assert _raises_value_error(kmeans_plus_plus_init, np.zeros((3, 2)), 4, 0)


def test_returns_a_copy_not_a_view():
    X = _two_blobs()
    centers = kmeans_plus_plus_init(X, 2, seed=0)
    centers[:] = -1.0
    assert not np.any(X == -1.0)


def test_does_not_modify_the_data():
    X = _two_blobs()
    before = X.copy()
    kmeans_plus_plus_init(X, 3, seed=4)
    assert np.array_equal(X, before)


def test_different_seeds_can_pick_different_centers():
    X = _two_blobs()
    seen = {tuple(kmeans_plus_plus_init(X, 3, seed=s).ravel()) for s in range(10)}
    assert len(seen) > 1


def test_accepts_a_python_list_input():
    centers = kmeans_plus_plus_init([[0.0, 0.0], [5.0, 5.0]], 2, seed=0)
    assert centers.shape == (2, 2)
