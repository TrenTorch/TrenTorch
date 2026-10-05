"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mse_gradient = _module.mse_gradient
make_batches = _module.make_batches
mini_batch_gradient_descent = _module.mini_batch_gradient_descent


def _dataset(seed=0, m=40, d=3):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(m, d))
    w_true = np.array([2.0, -1.0, 0.5])[:d]
    return X, X @ w_true, w_true


def _reference(X, y, w0, lr, batch_size, epochs, seed):
    # An independent re-implementation, written with explicit indexing.
    rng = np.random.default_rng(seed)
    m = len(y)
    w = np.array(w0, dtype=float)
    out = [w.copy()]
    for _ in range(epochs):
        order = rng.permutation(m)
        for start in range(0, m, batch_size):
            idx = order[start : start + batch_size]
            residual = X[idx] @ w - y[idx]
            w = w - lr * (2.0 / len(idx)) * (X[idx].T @ residual)
            out.append(w.copy())
    return out


# ---- 1-3: the gradient ----


def test_1_gradient_matches_a_hand_computed_case():
    X = np.array([[1.0], [2.0]])
    y = np.array([1.0, 2.0])
    # residuals are [-1, -2], so (2/2) * (1*-1 + 2*-2) = -5
    np.testing.assert_allclose(mse_gradient(X, y, np.array([0.0])), [-5.0])


def test_2_gradient_matches_finite_differences():
    X, y, _ = _dataset()
    w = np.array([0.3, -0.7, 1.1])
    loss = lambda v: np.mean((X @ v - y) ** 2)
    eps = 1e-6
    numeric = np.array([(loss(w + eps * e) - loss(w - eps * e)) / (2 * eps) for e in np.eye(3)])
    np.testing.assert_allclose(mse_gradient(X, y, w), numeric, atol=1e-5)


def test_3_gradient_is_zero_at_the_exact_solution():
    X, y, w_true = _dataset()
    np.testing.assert_allclose(mse_gradient(X, y, w_true), np.zeros(3), atol=1e-12)


# ---- 4-6: batching ----


def test_4_batches_cover_every_index_exactly_once():
    batches = make_batches(10, 4, np.random.default_rng(0))
    assert sorted(np.concatenate(batches).tolist()) == list(range(10))


def test_5_batch_sizes_with_a_shorter_final_batch():
    batches = make_batches(10, 4, np.random.default_rng(0))
    assert [len(b) for b in batches] == [4, 4, 2]


def test_6_batch_size_larger_than_the_dataset_gives_one_batch():
    batches = make_batches(5, 100, np.random.default_rng(0))
    assert len(batches) == 1 and len(batches[0]) == 5


def test_7_batches_follow_one_permutation_draw():
    batches = make_batches(9, 3, np.random.default_rng(7))
    expected = np.random.default_rng(7).permutation(9)
    np.testing.assert_array_equal(np.concatenate(batches), expected)


# ---- 8-12: the loop ----


def test_8_one_epoch_on_independent_features_is_order_free():
    # With X = identity, row i only ever touches weight i, so after one
    # epoch each weight has moved by exactly lr * (y_i - 0) = 0.5 * y_i
    # no matter how the rows were shuffled or batched.
    X = np.eye(4)
    y = np.array([2.0, 4.0, 6.0, 8.0])
    trajectory = mini_batch_gradient_descent(X, y, np.zeros(4), 0.5, 2, 1, np.random.default_rng(0))
    np.testing.assert_allclose(trajectory[-1], [1.0, 2.0, 3.0, 4.0])


def test_9_trajectory_length_counts_every_update():
    X, y, _ = _dataset(m=10)
    trajectory = mini_batch_gradient_descent(X, y, np.zeros(3), 0.01, 4, 3, np.random.default_rng(0))
    assert len(trajectory) == 1 + 3 * 3  # ceil(10 / 4) = 3 batches per epoch


def test_10_matches_an_independent_reference_with_a_short_last_batch():
    X, y, _ = _dataset(m=11)
    w0 = np.array([0.5, 0.5, 0.5])
    got = mini_batch_gradient_descent(X, y, w0, 0.05, 4, 3, np.random.default_rng(3))
    want = _reference(X, y, w0, 0.05, 4, 3, 3)
    np.testing.assert_allclose(got, want, atol=1e-10)


def test_11_full_batch_equals_standard_gradient_descent():
    X, y, _ = _dataset(m=12)
    w = np.zeros(3)
    expected = [w.copy()]
    for _ in range(5):
        w = w - 0.05 * (2.0 / 12) * X.T @ (X @ w - y)
        expected.append(w.copy())
    got = mini_batch_gradient_descent(X, y, np.zeros(3), 0.05, 12, 5, np.random.default_rng(1))
    np.testing.assert_allclose(got, expected, atol=1e-10)


def test_12_converges_on_noise_free_data():
    X, y, w_true = _dataset(m=50)
    trajectory = mini_batch_gradient_descent(X, y, np.zeros(3), 0.05, 10, 200, np.random.default_rng(0))
    np.testing.assert_allclose(trajectory[-1], w_true, atol=1e-3)


# ---- mutation-catching ----


def test_13_inputs_are_not_modified():
    X, y, _ = _dataset(m=10)
    w0 = np.array([1.0, 2.0, 3.0])
    X_copy, y_copy, w_copy = X.copy(), y.copy(), w0.copy()
    mini_batch_gradient_descent(X, y, w0, 0.05, 3, 2, np.random.default_rng(0))
    np.testing.assert_array_equal(X, X_copy)
    np.testing.assert_array_equal(y, y_copy)
    np.testing.assert_array_equal(w0, w_copy)


def test_14_trajectory_entries_are_independent_arrays():
    X, y, _ = _dataset(m=10)
    trajectory = mini_batch_gradient_descent(X, y, np.zeros(3), 0.05, 5, 2, np.random.default_rng(0))
    assert not np.allclose(trajectory[0], trajectory[-1])
    assert all(trajectory[i] is not trajectory[i + 1] for i in range(len(trajectory) - 1))


def test_15_different_seeds_take_different_paths():
    X, y, _ = _dataset(m=20)
    a = mini_batch_gradient_descent(X, y, np.zeros(3), 0.05, 4, 1, np.random.default_rng(0))
    b = mini_batch_gradient_descent(X, y, np.zeros(3), 0.05, 4, 1, np.random.default_rng(1))
    assert not np.allclose(a[1], b[1])
