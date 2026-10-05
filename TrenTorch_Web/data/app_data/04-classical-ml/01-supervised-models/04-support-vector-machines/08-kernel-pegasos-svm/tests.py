"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
kernel_pegasos = _module.kernel_pegasos


def _separable_problem(seed=0, n=60):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 2))
    y = np.where(X[:, 0] + X[:, 1] > 0, 1.0, -1.0)
    K = X @ X.T
    return X, y, K


def test_first_step_always_updates_the_first_point():
    # With no coefficients yet, the decision is 0, so the margin is violated.
    K = np.ones((2, 2))
    y = np.array([1.0, -1.0])
    alpha = kernel_pegasos(K, y, lam=1.0, iterations=1)
    assert np.allclose(alpha, [1.0, 0.0])


def test_zero_iterations_returns_all_zeros():
    _, y, K = _separable_problem(n=10)
    alpha = kernel_pegasos(K, y, lam=0.1, iterations=0)
    assert np.allclose(alpha, np.zeros(10))


def test_returns_a_float_array_of_length_n():
    _, y, K = _separable_problem(n=12)
    alpha = kernel_pegasos(K, y, lam=0.1, iterations=50)
    assert alpha.shape == (12,)
    assert np.issubdtype(alpha.dtype, np.floating)


def test_coefficients_are_non_negative_whole_numbers():
    _, y, K = _separable_problem(n=20)
    alpha = kernel_pegasos(K, y, lam=0.05, iterations=500)
    assert np.all(alpha >= 0.0)
    assert np.allclose(alpha, np.round(alpha))


def test_total_updates_never_exceed_the_iteration_count():
    _, y, K = _separable_problem(n=20)
    alpha = kernel_pegasos(K, y, lam=0.05, iterations=300)
    assert alpha.sum() <= 300


def test_exact_trace_with_all_ones_kernel():
    # K is all ones, y is all +1, lam = 1.
    # t=1 i=0: decision 0 -> alpha = [1, 0]
    # t=2 i=1: decision 1/2 -> alpha = [1, 1]
    # t=3 i=0: decision 2/3 -> alpha = [2, 1]
    # t=4 i=1: decision 3/4 -> alpha = [2, 2]
    K = np.ones((2, 2))
    y = np.ones(2)
    alpha = kernel_pegasos(K, y, lam=1.0, iterations=4)
    assert np.allclose(alpha, [2.0, 2.0])


def test_comfortably_correct_points_do_not_get_updated():
    # Huge kernel values make the decision far past the margin after one update.
    # t=1 i=0 updates; t=2 i=1 decision is 50 (margin satisfied); t=3, t=4 are satisfied too.
    K = np.full((2, 2), 100.0)
    y = np.ones(2)
    alpha = kernel_pegasos(K, y, lam=1.0, iterations=4)
    assert np.allclose(alpha, [1.0, 0.0])


def test_is_deterministic():
    _, y, K = _separable_problem(n=25, seed=3)
    first = kernel_pegasos(K, y, lam=0.02, iterations=400)
    second = kernel_pegasos(K, y, lam=0.02, iterations=400)
    assert np.array_equal(first, second)


def test_does_not_modify_its_inputs():
    _, y, K = _separable_problem(n=15)
    K_before, y_before = K.copy(), y.copy()
    kernel_pegasos(K, y, lam=0.1, iterations=100)
    assert np.array_equal(K, K_before)
    assert np.array_equal(y, y_before)


def test_learns_a_separable_problem_with_a_linear_gram_matrix():
    X, y, K = _separable_problem(seed=4, n=80)
    alpha = kernel_pegasos(K, y, lam=0.01, iterations=5000)
    scores = K @ (alpha * y)
    accuracy = (np.sign(scores) == y).mean()
    assert accuracy > 0.9


def test_huge_lambda_keeps_every_step_inside_the_margin_so_every_step_updates():
    # The decision is divided by lam * t, so with a huge lam it stays near zero,
    # every step violates the margin, and the coefficients sum to the iteration count.
    _, y, K = _separable_problem(seed=5, n=40)
    alpha = kernel_pegasos(K, y, lam=1e6, iterations=200)
    assert alpha.sum() == 200.0


def test_exact_trace_with_identity_kernel_and_mixed_labels():
    # K is the identity, y = [+1, -1], lam = 1.
    # t=1 i=0: decision 0 -> alpha = [1, 0]
    # t=2 i=1: decision 0 -> alpha = [1, 1]
    # t=3 i=0: decision (1 * 1) / 3 = 1/3 -> alpha = [2, 1]
    K = np.eye(2)
    y = np.array([1.0, -1.0])
    alpha = kernel_pegasos(K, y, lam=1.0, iterations=3)
    assert np.allclose(alpha, [2.0, 1.0])
