"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
svr_objective = _module.svr_objective
svr_gradient = _module.svr_gradient
train_linear_svr = _module.train_linear_svr


def test_objective_is_only_the_l2_term_when_every_point_is_inside_the_tube():
    weight = np.array([0.5, 0.5])
    X = np.array([[1.0, 1.0], [2.0, 0.0]])
    y = X @ weight  # exact fit, residual zero
    result = svr_objective(weight, 0.0, X, y, epsilon=0.1, lambda_reg=0.2)
    assert np.isclose(result, 0.2 * np.dot(weight, weight))


def test_objective_charges_points_outside_the_tube():
    # weight = [1], bias = 0, one point x = 3 with target 0: residual 3, loss 3 - 0.5 = 2.5
    X = np.array([[3.0]])
    y = np.array([0.0])
    assert np.isclose(svr_objective(np.array([1.0]), 0.0, X, y, epsilon=0.5, lambda_reg=0.0), 2.5)


def test_gradient_is_zero_for_points_inside_the_tube():
    weight = np.array([1.0])
    X = np.array([[1.0]])
    y = np.array([1.05])  # residual -0.05, inside tube of 0.1
    grad_weight, grad_bias = svr_gradient(weight, 0.0, X, y, epsilon=0.1, lambda_reg=0.0)
    assert np.isclose(grad_weight[0], 0.0)
    assert np.isclose(grad_bias, 0.0)


def test_gradient_matches_finite_differences_away_from_the_tube_edges():
    rng = np.random.default_rng(0)
    weight = rng.normal(size=3)
    bias = 0.2
    X = rng.normal(size=(15, 3)) * 3.0
    y = rng.normal(size=15) * 3.0
    epsilon, lambda_reg = 0.1, 0.05

    grad_weight, grad_bias = svr_gradient(weight, bias, X, y, epsilon, lambda_reg)

    eps = 1e-6
    numeric = np.empty(3)
    for i in range(3):
        w_plus, w_minus = weight.copy(), weight.copy()
        w_plus[i] += eps
        w_minus[i] -= eps
        numeric[i] = (
            svr_objective(w_plus, bias, X, y, epsilon, lambda_reg)
            - svr_objective(w_minus, bias, X, y, epsilon, lambda_reg)
        ) / (2 * eps)
    numeric_bias = (
        svr_objective(weight, bias + eps, X, y, epsilon, lambda_reg)
        - svr_objective(weight, bias - eps, X, y, epsilon, lambda_reg)
    ) / (2 * eps)

    assert np.allclose(grad_weight, numeric, atol=1e-4)
    assert np.isclose(grad_bias, numeric_bias, atol=1e-4)


def test_gradient_uses_the_sign_of_the_residual_outside_the_tube():
    # residual = 1 * 3 - 0 = 3 (outside), so the direction is +1 and grad_weight = x = 3
    grad_weight, grad_bias = svr_gradient(np.array([1.0]), 0.0, np.array([[3.0]]), np.array([0.0]), 0.1, 0.0)
    assert np.isclose(grad_weight[0], 3.0)
    assert np.isclose(grad_bias, 1.0)


def test_regularization_adds_its_gradient_term():
    weight = np.array([2.0])
    grad_weight, _ = svr_gradient(weight, 0.0, np.array([[0.0]]), np.array([0.0]), 0.1, lambda_reg=0.5)
    assert np.isclose(grad_weight[0], 2.0 * 0.5 * 2.0)


def test_training_fits_a_noise_free_line_within_the_tube():
    rng = np.random.default_rng(1)
    X = rng.uniform(-1.0, 1.0, size=(60, 1))
    y = 2.0 * X[:, 0] + 1.0
    weight, bias = train_linear_svr(X, y, lr=0.1, epochs=3000, epsilon=0.05, lambda_reg=0.0)
    predictions = X @ weight + bias
    assert np.all(np.abs(predictions - y) <= 0.1)


def test_training_returns_a_weight_vector_and_a_scalar_bias():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(20, 3))
    y = X @ np.array([1.0, -1.0, 0.5])
    weight, bias = train_linear_svr(X, y, lr=0.05, epochs=100)
    assert weight.shape == (3,)
    assert np.isscalar(bias) or np.ndim(bias) == 0


def test_zero_epochs_returns_zero_parameters():
    X = np.ones((4, 2))
    y = np.ones(4)
    weight, bias = train_linear_svr(X, y, epochs=0)
    assert np.allclose(weight, 0.0)
    assert np.isclose(bias, 0.0)


def test_larger_regularization_shrinks_the_weights():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(50, 2))
    y = X @ np.array([3.0, -2.0])
    weak, _ = train_linear_svr(X, y, lr=0.05, epochs=800, epsilon=0.05, lambda_reg=0.0)
    strong, _ = train_linear_svr(X, y, lr=0.05, epochs=800, epsilon=0.05, lambda_reg=5.0)
    assert np.linalg.norm(strong) < np.linalg.norm(weak)


def test_objective_is_nonnegative():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(10, 2))
    y = rng.normal(size=10)
    assert svr_objective(rng.normal(size=2), 0.1, X, y, epsilon=0.2, lambda_reg=0.1) >= 0.0


def test_gradient_does_not_modify_its_inputs():
    weight = np.array([0.4, -0.2])
    X = np.array([[1.0, 2.0], [0.5, -1.0]])
    y = np.array([0.0, 1.0])
    weight_before = weight.copy()
    svr_gradient(weight, 0.0, X, y, 0.1, 0.1)
    assert np.array_equal(weight, weight_before)
