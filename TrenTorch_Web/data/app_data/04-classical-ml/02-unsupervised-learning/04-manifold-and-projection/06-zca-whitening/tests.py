"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

zca_whiten = load_solution(__file__).zca_whiten


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _correlated():
    rng = np.random.default_rng(0)
    A = np.array([[2.0, 0.0, 0.0], [1.0, 1.5, 0.0], [0.5, -0.5, 0.8]])
    return rng.normal(size=(300, 3)) @ A.T + np.array([4.0, -2.0, 1.0])


def test_output_shape_matches_input():
    X = _correlated()
    assert zca_whiten(X).shape == X.shape


def test_output_is_centered():
    assert np.allclose(zca_whiten(_correlated()).mean(axis=0), 0.0, atol=1e-9)


def test_output_covariance_is_identity():
    Y = zca_whiten(_correlated())
    cov = Y.T @ Y / (len(Y) - 1)
    assert np.allclose(cov, np.eye(3), atol=1e-6)


def test_whitening_already_white_data_changes_nothing():
    X = _correlated()
    Y = zca_whiten(X, eps=0.0)
    Z = zca_whiten(Y, eps=0.0)
    assert np.allclose(Z, Y, atol=1e-8)


def test_zca_stays_closer_to_the_centered_input_than_pca_whitening():
    X = _correlated()
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / (len(X) - 1)
    vals, vecs = np.linalg.eigh(C)
    pca_white = Xc @ vecs @ np.diag(1.0 / np.sqrt(vals)) @ vecs.T
    zca = zca_whiten(X)
    assert np.linalg.norm(zca - Xc) <= np.linalg.norm(pca_white - Xc) + 1e-9


def test_same_input_gives_same_output():
    X = _correlated()
    assert np.array_equal(zca_whiten(X), zca_whiten(X))


def test_single_row_raises():
    assert _raises_value_error(zca_whiten, np.array([[1.0, 2.0]]))


def test_negative_eps_raises():
    assert _raises_value_error(zca_whiten, _correlated(), eps=-1.0)


def test_does_not_modify_the_data():
    X = _correlated()
    before = X.copy()
    zca_whiten(X)
    assert np.array_equal(X, before)
