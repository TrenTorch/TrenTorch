"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
lle_weights = _module.lle_weights
lle_embedding = _module.lle_embedding

LINE = np.arange(5, dtype=float).reshape(-1, 1)


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_weight_matrix_is_square():
    assert lle_weights(LINE, 2).shape == (5, 5)


def test_each_row_sums_to_one():
    rng = np.random.default_rng(0)
    W = lle_weights(rng.normal(size=(10, 3)), 3)
    assert np.allclose(W.sum(axis=1), 1.0)


def test_diagonal_is_zero_and_each_row_has_k_nonzeros():
    rng = np.random.default_rng(1)
    W = lle_weights(rng.normal(size=(10, 3)), 3)
    assert np.all(np.diag(W) == 0.0)
    assert np.all(np.count_nonzero(W, axis=1) == 3)


def test_interior_points_on_a_line_get_half_weight_on_each_side():
    W = lle_weights(LINE, 2)
    assert np.allclose(W[2, [1, 3]], [0.5, 0.5])


def test_interior_points_on_a_line_reconstruct_exactly():
    W = lle_weights(LINE, 2)
    for i in [1, 2, 3]:
        assert np.isclose(W[i] @ LINE[:, 0], LINE[i, 0], atol=1e-9)


def test_translating_the_data_leaves_weights_unchanged():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(9, 2))
    assert np.allclose(lle_weights(X + 5.0, 3), lle_weights(X, 3))


def test_scaling_the_data_leaves_weights_unchanged():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(9, 2))
    assert np.allclose(lle_weights(3.0 * X, 3), lle_weights(X, 3))


def test_duplicate_points_give_finite_weights():
    X = np.array([[0.0], [0.0], [1.0], [2.0]])
    W = lle_weights(X, 1)
    assert np.all(np.isfinite(W))
    assert np.allclose(W.sum(axis=1), 1.0)


def test_k_outside_range_raises():
    assert _raises_value_error(lle_weights, LINE, 0)
    assert _raises_value_error(lle_weights, LINE, 5)


def test_non_matrix_input_raises():
    assert _raises_value_error(lle_weights, np.arange(5.0), 2)


def test_embedding_has_requested_shape():
    rng = np.random.default_rng(4)
    W = lle_weights(rng.normal(size=(12, 3)), 4)
    assert lle_embedding(W, 2).shape == (12, 2)


def test_embedding_columns_are_orthonormal_and_centred():
    rng = np.random.default_rng(5)
    W = lle_weights(rng.normal(size=(12, 3)), 4)
    Y = lle_embedding(W, 2)
    assert np.allclose(Y.T @ Y, np.eye(2), atol=1e-8)
    assert np.allclose(Y.sum(axis=0), 0.0, atol=1e-8)


def test_one_dimensional_embedding_recovers_the_line_order():
    W = lle_weights(LINE, 2)
    Y = lle_embedding(W, 1)
    assert abs(np.corrcoef(Y[:, 0], LINE[:, 0])[0, 1]) > 0.95


def test_embedding_rejects_non_square_weights():
    assert _raises_value_error(lle_embedding, np.zeros((4, 3)), 1)


def test_embedding_rejects_out_of_range_dimension():
    W = lle_weights(LINE, 2)
    assert _raises_value_error(lle_embedding, W, 0)
    assert _raises_value_error(lle_embedding, W, 5)


def test_inputs_are_not_modified():
    X = LINE.copy()
    lle_weights(X, 2)
    assert np.array_equal(X, LINE)
