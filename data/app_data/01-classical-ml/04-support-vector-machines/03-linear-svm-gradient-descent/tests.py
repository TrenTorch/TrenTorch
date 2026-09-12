"""
pytest data/app_data/01-classical-ml/04-support-vector-machines/03-linear-svm-gradient-descent/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-support-vector-machines/{Path(__file__).resolve().parent.name}")
svm_objective = _module.svm_objective
svm_gradient = _module.svm_gradient
train_linear_svm = _module.train_linear_svm


def test_svm_objective_is_purely_the_l2_term_when_all_points_have_zero_loss():
    weight = np.array([0.5, 0.5])
    bias = 0.0
    x = np.array([[10.0, 10.0], [-10.0, -10.0]])
    y = np.array([1.0, -1.0])
    result = svm_objective(weight, bias, x, y, lambda_reg=0.1)
    expected_l2 = 0.1 * np.dot(weight, weight)
    assert np.isclose(result, expected_l2, atol=1e-6)


def test_svm_gradient_matches_finite_difference_of_objective():
    rng = np.random.default_rng(0)
    weight = rng.normal(size=3)
    bias = 0.3
    x = rng.normal(size=(20, 3))
    y = np.sign(rng.normal(size=20))
    y[y == 0] = 1.0
    lambda_reg = 0.05

    grad_weight, grad_bias = svm_gradient(weight, bias, x, y, lambda_reg)

    eps = 1e-5
    numeric_grad_weight = np.empty(3)
    for i in range(3):
        w_plus, w_minus = weight.copy(), weight.copy()
        w_plus[i] += eps
        w_minus[i] -= eps
        numeric_grad_weight[i] = (
            svm_objective(w_plus, bias, x, y, lambda_reg) - svm_objective(w_minus, bias, x, y, lambda_reg)
        ) / (2 * eps)
    numeric_grad_bias = (
        svm_objective(weight, bias + eps, x, y, lambda_reg)
        - svm_objective(weight, bias - eps, x, y, lambda_reg)
    ) / (2 * eps)

    assert np.allclose(grad_weight, numeric_grad_weight, atol=1e-4)
    assert np.isclose(grad_bias, numeric_grad_bias, atol=1e-4)


def test_svm_gradient_ignores_points_that_are_comfortably_correct():
    # A point with margin >= 1 contributes zero to the hinge part of
    # the gradient. Only the L2 term's gradient should remain.
    weight = np.array([1.0])
    bias = 0.0
    x = np.array([[10.0]])  # margin = 1*(10) = 10, comfortably correct
    y = np.array([1.0])
    grad_weight, grad_bias = svm_gradient(weight, bias, x, y, lambda_reg=0.1)
    assert np.isclose(grad_weight[0], 2.0 * 0.1 * 1.0)  # pure L2 gradient
    assert np.isclose(grad_bias, 0.0)


def test_train_linear_svm_achieves_high_accuracy_on_separable_data():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(200, 2))
    y = np.where(x[:, 0] + x[:, 1] > 0, 1.0, -1.0)

    weight, bias = train_linear_svm(x, y, lr=0.1, epochs=500, lambda_reg=0.001)
    predictions = np.sign(x @ weight + bias)
    accuracy = (predictions == y).mean()
    assert accuracy > 0.95


def test_larger_lambda_reg_produces_a_smaller_weight_norm():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(150, 3))
    y = np.where(x[:, 0] > 0, 1.0, -1.0)

    weak_reg_weight, _ = train_linear_svm(x, y, lr=0.1, epochs=300, lambda_reg=0.001)
    strong_reg_weight, _ = train_linear_svm(x, y, lr=0.1, epochs=300, lambda_reg=1.0)
    assert np.linalg.norm(strong_reg_weight) < np.linalg.norm(weak_reg_weight)


def test_svm_gradient_uses_the_correct_margin_violation_condition():
    # Directly targets a mutant that flips the margin-violation
    # comparison (e.g. margin > 1 instead of margin < 1): the point set
    # up here has margin exactly 0.5 (clearly violating), the correct
    # gradient must reflect that violation, not treat it as satisfied.
    weight = np.array([1.0])
    bias = 0.0
    x = np.array([[0.5]])  # margin = 1*(0.5) = 0.5 < 1, violates
    y = np.array([1.0])
    grad_weight, grad_bias = svm_gradient(weight, bias, x, y, lambda_reg=0.0)
    # violating point contributes -target*x = -0.5 to grad_weight
    assert np.isclose(grad_weight[0], -0.5)
    assert np.isclose(grad_bias, -1.0)
