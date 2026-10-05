"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sample_gradient = _module.sample_gradient
stochastic_gradient_descent = _module.stochastic_gradient_descent


def _dataset(seed=0, m=40, d=3):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(m, d))
    w_true = np.array([2.0, -1.0, 0.5])[:d]
    return X, X @ w_true, w_true


# ---- 1-3: the single-example gradient ----


def test_1_gradient_matches_a_hand_computed_case():
    # x = [1, 2], w = [1, 1], y = 1: prediction 3, residual 2
    # gradient = 2 * 2 * [1, 2] = [4, 8]
    result = sample_gradient(np.array([1.0, 2.0]), 1.0, np.array([1.0, 1.0]))
    np.testing.assert_allclose(result, [4.0, 8.0])


def test_2_gradient_matches_finite_differences():
    x = np.array([0.5, -1.5, 2.0])
    w = np.array([0.3, -0.7, 1.1])
    loss = lambda v: (x @ v - 4.0) ** 2
    eps = 1e-6
    numeric = np.array([(loss(w + eps * e) - loss(w - eps * e)) / (2 * eps) for e in np.eye(3)])
    np.testing.assert_allclose(sample_gradient(x, 4.0, w), numeric, atol=1e-5)


def test_3_gradient_is_zero_when_the_example_is_fit_exactly():
    x = np.array([1.0, 2.0])
    np.testing.assert_allclose(sample_gradient(x, 5.0, np.array([1.0, 2.0])), np.zeros(2))


# ---- 4-9: the loop ----


def test_4_trajectory_length_is_one_plus_epochs_times_samples():
    X, y, _ = _dataset(m=7)
    trajectory = stochastic_gradient_descent(X, y, np.zeros(3), 0.01, 3, np.random.default_rng(0))
    assert len(trajectory) == 1 + 3 * 7


def test_5_trajectory_starts_at_w0():
    X, y, _ = _dataset(m=7)
    w0 = np.array([1.0, 2.0, 3.0])
    trajectory = stochastic_gradient_descent(X, y, w0, 0.01, 1, np.random.default_rng(0))
    np.testing.assert_array_equal(trajectory[0], w0)


def test_6_every_example_is_used_exactly_once_per_epoch():
    # With X = identity, example i only moves weight i. With lr = 0.5 each
    # weight lands exactly on y_i if (and only if) it was updated once.
    X = np.eye(5)
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    trajectory = stochastic_gradient_descent(X, y, np.zeros(5), 0.5, 1, np.random.default_rng(0))
    np.testing.assert_allclose(trajectory[-1], y)


def test_7_each_update_changes_the_weights_using_one_example():
    X = np.eye(3)
    y = np.array([2.0, 4.0, 6.0])
    trajectory = stochastic_gradient_descent(X, y, np.zeros(3), 0.25, 1, np.random.default_rng(0))
    for before, after in zip(trajectory, trajectory[1:]):
        assert np.count_nonzero(after - before) == 1


def test_8_matches_an_independent_reference():
    X, y, _ = _dataset(m=9)
    w0 = np.array([0.5, 0.5, 0.5])
    got = stochastic_gradient_descent(X, y, w0, 0.02, 3, np.random.default_rng(5))

    rng = np.random.default_rng(5)
    w = w0.copy()
    want = [w.copy()]
    for _ in range(3):
        for i in rng.permutation(9):
            w = w - 0.02 * 2.0 * (X[i] @ w - y[i]) * X[i]
            want.append(w.copy())
    np.testing.assert_allclose(got, want, atol=1e-10)


def test_9_converges_on_noise_free_data():
    X, y, w_true = _dataset(m=50)
    trajectory = stochastic_gradient_descent(X, y, np.zeros(3), 0.02, 100, np.random.default_rng(0))
    np.testing.assert_allclose(trajectory[-1], w_true, atol=1e-3)


# ---- mutation-catching ----


def test_10_inputs_are_not_modified():
    X, y, _ = _dataset(m=10)
    w0 = np.array([1.0, 2.0, 3.0])
    X_copy, y_copy, w_copy = X.copy(), y.copy(), w0.copy()
    stochastic_gradient_descent(X, y, w0, 0.01, 2, np.random.default_rng(0))
    np.testing.assert_array_equal(X, X_copy)
    np.testing.assert_array_equal(y, y_copy)
    np.testing.assert_array_equal(w0, w_copy)


def test_11_different_seeds_take_different_paths():
    X, y, _ = _dataset(m=20)
    a = stochastic_gradient_descent(X, y, np.zeros(3), 0.02, 1, np.random.default_rng(0))
    b = stochastic_gradient_descent(X, y, np.zeros(3), 0.02, 1, np.random.default_rng(1))
    assert not np.allclose(a[1], b[1])


def test_12_a_shuffled_epoch_does_not_always_visit_in_row_order():
    # A wrong implementation looping over range(m) would give the same
    # first step for every seed, since it always starts with row 0.
    X, y, _ = _dataset(m=20)
    firsts = [
        stochastic_gradient_descent(X, y, np.zeros(3), 0.02, 1, np.random.default_rng(seed))[1]
        for seed in range(5)
    ]
    assert any(not np.allclose(firsts[0], other) for other in firsts[1:])
