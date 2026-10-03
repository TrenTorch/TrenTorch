"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mahalanobis = _module.mahalanobis


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_identity_covariance_gives_euclidean_distance():
    assert np.isclose(mahalanobis([3.0, 4.0], [0.0, 0.0], np.eye(2)), 5.0)


def test_diagonal_covariance_scales_each_axis():
    cov = np.diag([4.0, 1.0])
    assert np.isclose(mahalanobis([2.0, 0.0], [0.0, 0.0], cov), 1.0)
    assert np.isclose(mahalanobis([0.0, 2.0], [0.0, 0.0], cov), 2.0)


def test_one_dimensional_case_is_standardized_difference():
    assert np.isclose(mahalanobis([2.0], [0.0], [[4.0]]), 1.0)


def test_full_covariance_hand_example():
    # cov^-1 = (1/3) [[2, -1], [-1, 2]], so d^2 = (1/3) * 2 for diff = (1, 0).
    cov = np.array([[2.0, 1.0], [1.0, 2.0]])
    assert np.isclose(mahalanobis([1.0, 0.0], [0.0, 0.0], cov), np.sqrt(2 / 3))


def test_identical_points_have_zero_distance():
    assert mahalanobis([1.0, 2.0], [1.0, 2.0], np.eye(2)) == 0.0


def test_distance_is_symmetric():
    cov = np.array([[2.0, 0.5], [0.5, 1.0]])
    x, y = np.array([1.0, -1.0]), np.array([0.2, 0.7])
    assert np.isclose(mahalanobis(x, y, cov), mahalanobis(y, x, cov))


def test_scaling_data_and_covariance_together_leaves_distance_unchanged():
    cov = np.array([[2.0, 0.5], [0.5, 1.0]])
    x, y = np.array([1.0, -1.0]), np.array([0.2, 0.7])
    assert np.isclose(mahalanobis(3 * x, 3 * y, 9 * cov), mahalanobis(x, y, cov))


def test_translating_both_points_leaves_distance_unchanged():
    cov = np.array([[2.0, 0.5], [0.5, 1.0]])
    x, y = np.array([1.0, -1.0]), np.array([0.2, 0.7])
    shift = np.array([5.0, 9.0])
    assert np.isclose(mahalanobis(x + shift, y + shift, cov), mahalanobis(x, y, cov))


def test_matches_euclidean_distance_after_cholesky_whitening():
    cov = np.array([[2.0, 0.5], [0.5, 1.0]])
    x, y = np.array([1.0, -1.0]), np.array([0.2, 0.7])
    L = np.linalg.cholesky(cov)
    whitened = np.linalg.solve(L, x - y)
    assert np.isclose(mahalanobis(x, y, cov), np.linalg.norm(whitened))


def test_triangle_inequality_holds_for_random_positive_definite_covariance():
    rng = np.random.default_rng(0)
    A = rng.normal(size=(3, 3))
    cov = A @ A.T + np.eye(3)
    for _ in range(20):
        x, y, z = rng.normal(size=(3, 3))
        assert mahalanobis(x, z, cov) <= mahalanobis(x, y, cov) + mahalanobis(y, z, cov) + 1e-9


def test_non_symmetric_covariance_raises():
    assert _raises_value_error(mahalanobis, [1.0, 0.0], [0.0, 0.0], [[1.0, 2.0], [0.0, 1.0]])


def test_non_positive_definite_covariance_raises():
    assert _raises_value_error(mahalanobis, [1.0, 0.0], [0.0, 0.0], [[1.0, 2.0], [2.0, 1.0]])


def test_covariance_shape_mismatch_raises():
    assert _raises_value_error(mahalanobis, [1.0, 0.0], [0.0, 0.0], np.eye(3))


def test_inputs_are_not_modified():
    cov = np.array([[2.0, 0.5], [0.5, 1.0]])
    x = np.array([1.0, -1.0])
    y = np.array([0.2, 0.7])
    cov0, x0, y0 = cov.copy(), x.copy(), y.copy()
    mahalanobis(x, y, cov)
    assert np.array_equal(cov, cov0) and np.array_equal(x, x0) and np.array_equal(y, y0)
