"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

fuzzy_c_means = load_solution(__file__).fuzzy_c_means


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _two_blobs():
    a = np.array([[0.0, 0.0], [0.2, 0.0], [0.0, 0.2], [0.2, 0.2]])
    b = np.array([[10.0, 10.0], [10.2, 10.0], [10.0, 10.2], [10.2, 10.2]])
    return np.vstack([a, b])


def test_centers_have_shape_c_by_d():
    centers, U = fuzzy_c_means(_two_blobs(), 2)
    assert centers.shape == (2, 2)
    assert U.shape == (8, 2)


def test_memberships_sum_to_one_per_row():
    _, U = fuzzy_c_means(_two_blobs(), 2)
    assert np.allclose(U.sum(axis=1), 1.0)


def test_memberships_are_nonnegative():
    _, U = fuzzy_c_means(_two_blobs(), 2)
    assert np.all(U >= 0)


def test_centers_land_on_the_blob_means():
    centers, _ = fuzzy_c_means(_two_blobs(), 2)
    targets = np.array([[0.1, 0.1], [10.1, 10.1]])
    for t in targets:
        assert np.min(np.linalg.norm(centers - t, axis=1)) < 0.05


def test_points_are_confidently_assigned_to_their_blob():
    _, U = fuzzy_c_means(_two_blobs(), 2)
    assert np.all(U[:4].max(axis=1) > 0.99)
    assert np.all(U[4:].max(axis=1) > 0.99)


def test_blob_points_prefer_different_clusters():
    _, U = fuzzy_c_means(_two_blobs(), 2)
    assert np.argmax(U[0]) != np.argmax(U[4])


def test_point_midway_between_two_centers_is_split_evenly():
    X = np.array([[0.0, 0.0], [10.0, 0.0], [5.0, 0.0]])
    centers, U = fuzzy_c_means(X, 2)
    left = np.argmin(centers[:, 0])
    right = 1 - left
    assert abs(U[2, left] - U[2, right]) < 0.05


def test_exact_center_point_gets_full_membership():
    X = np.array([[0.0, 0.0], [0.0, 0.1], [9.0, 9.0], [9.0, 9.1]])
    _, U = fuzzy_c_means(X, 2)
    assert np.all(np.isfinite(U))
    assert np.allclose(U.sum(axis=1), 1.0)


def test_m_must_exceed_one():
    assert _raises_value_error(fuzzy_c_means, _two_blobs(), 2, m=1.0)


def test_c_out_of_range_raises():
    assert _raises_value_error(fuzzy_c_means, _two_blobs(), 0)
    assert _raises_value_error(fuzzy_c_means, _two_blobs(), 9)


def test_c_equal_one_gives_full_membership_everywhere():
    _, U = fuzzy_c_means(_two_blobs(), 1)
    assert np.allclose(U, 1.0)


def test_same_input_gives_same_result():
    c1, U1 = fuzzy_c_means(_two_blobs(), 2)
    c2, U2 = fuzzy_c_means(_two_blobs(), 2)
    assert np.array_equal(c1, c2)
    assert np.array_equal(U1, U2)


def test_does_not_modify_the_data():
    X = _two_blobs()
    before = X.copy()
    fuzzy_c_means(X, 2)
    assert np.array_equal(X, before)
