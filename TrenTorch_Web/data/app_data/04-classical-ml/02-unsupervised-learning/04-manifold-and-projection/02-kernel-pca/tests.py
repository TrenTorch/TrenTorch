"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

kernel_pca = load_solution(__file__).kernel_pca


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _data():
    return np.random.default_rng(0).normal(size=(12, 3))


def test_output_shape_is_n_by_components():
    Z = kernel_pca(_data(), 2)
    assert Z.shape == (12, 2)


def test_scores_are_centered():
    Z = kernel_pca(_data(), 2)
    assert np.allclose(Z.mean(axis=0), 0.0, atol=1e-9)


def test_linear_kernel_matches_pca_scores_up_to_sign():
    X = _data()
    Z = kernel_pca(X, 2)
    Xc = X - X.mean(axis=0)
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    pca = Xc @ Vt[:2].T
    for j in range(2):
        assert np.allclose(np.abs(Z[:, j]), np.abs(pca[:, j]), atol=1e-8)


def test_rbf_output_is_finite():
    Z = kernel_pca(_data(), 3, gamma=0.5)
    assert np.all(np.isfinite(Z))


def test_rbf_columns_have_decreasing_spread():
    Z = kernel_pca(_data(), 3, gamma=0.5)
    spreads = np.std(Z, axis=0)
    assert np.all(np.diff(spreads) <= 1e-9)


def test_one_component_on_one_dimensional_line_is_monotone_with_position():
    t = np.linspace(0.0, 1.0, 10)
    X = np.column_stack([t, np.zeros(10)])
    z = kernel_pca(X, 1)[:, 0]
    assert np.all(np.diff(z) > 0) or np.all(np.diff(z) < 0)


def test_components_out_of_range_raise():
    assert _raises_value_error(kernel_pca, _data(), 0)
    assert _raises_value_error(kernel_pca, _data(), 13)


def test_nonpositive_gamma_raises():
    assert _raises_value_error(kernel_pca, _data(), 2, gamma=0.0)
    assert _raises_value_error(kernel_pca, _data(), 2, gamma=-1.0)


def test_translation_does_not_change_absolute_scores():
    X = _data()
    a = np.abs(kernel_pca(X, 2))
    b = np.abs(kernel_pca(X + 3.0, 2))
    assert np.allclose(a, b, atol=1e-8)


def test_same_input_gives_same_scores():
    X = _data()
    assert np.array_equal(kernel_pca(X, 2, gamma=0.3), kernel_pca(X, 2, gamma=0.3))


def test_does_not_modify_the_data():
    X = _data()
    before = X.copy()
    kernel_pca(X, 2)
    assert np.array_equal(X, before)
