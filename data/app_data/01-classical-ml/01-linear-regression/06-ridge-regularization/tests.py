"""
pytest data/app_data/01-classical-ml/01-linear-regression/06-ridge-regularization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

ridge_grad = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).ridge_grad
mse_loss = load_solution("01-classical-ml/01-linear-regression/02-mse-loss").mse_loss
mse_gradient = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_gradient
gd_step = load_solution("01-classical-ml/01-linear-regression/04-gd-step").gd_step
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def test_lambda_zero_matches_plain_mse_gradient():
    rng = np.random.default_rng(7)
    input = rng.normal(size=(20, 4))
    weight = rng.normal(size=(1, 4))
    bias = np.zeros(1)
    target = rng.normal(size=(20, 1))
    grad_weight_plain, grad_bias_plain = mse_gradient(input, weight, bias, target)
    grad_weight_ridge, grad_bias_ridge = ridge_grad(input, weight, bias, target, lam=0.0)
    assert np.allclose(grad_weight_plain, grad_weight_ridge)
    assert np.allclose(grad_bias_plain, grad_bias_ridge)


def test_bias_gradient_is_never_penalized():
    rng = np.random.default_rng(8)
    input = rng.normal(size=(15, 3))
    weight = rng.normal(size=(1, 3))
    bias = np.zeros(1)
    target = rng.normal(size=(15, 1))
    _, grad_bias_plain = mse_gradient(input, weight, bias, target)
    _, grad_bias_ridge = ridge_grad(input, weight, bias, target, lam=5.0)
    assert np.allclose(grad_bias_plain, grad_bias_ridge)


def test_bias_none_still_returns_none_regardless_of_lambda():
    input = np.random.randn(10, 2)
    weight = np.random.randn(1, 2)
    target = np.random.randn(10, 1)
    _, grad_bias = ridge_grad(input, weight, None, target, lam=3.0)
    assert grad_bias is None


def test_matches_finite_difference_of_penalized_loss():
    rng = np.random.default_rng(9)
    input = rng.normal(size=(20, 3))
    weight = rng.normal(size=(1, 3))
    bias = np.zeros(1)
    target = rng.normal(size=(20, 1))
    lam = 0.5

    def penalized_loss(weight_):
        prediction = linear(input, weight_, bias)
        return mse_loss(prediction, target) + lam * np.sum(weight_**2)

    grad_weight, _ = ridge_grad(input, weight, bias, target, lam)
    eps = 1e-6
    for j in range(3):
        weight_plus, weight_minus = weight.copy(), weight.copy()
        weight_plus[0, j] += eps
        weight_minus[0, j] -= eps
        numerical = (penalized_loss(weight_plus) - penalized_loss(weight_minus)) / (2 * eps)
        assert np.isclose(grad_weight[0, j], numerical, atol=1e-4)


def test_larger_lambda_shrinks_weight_norm_after_training():
    # The actual point of ridge, checked end to end: on near-collinear
    # features, a bigger penalty must produce a smaller ||weight|| once
    # trained -- not just a bigger number plugged into an untested formula.
    rng = np.random.default_rng(10)
    n = 200
    base = rng.normal(size=n)
    input = np.column_stack([base, base + rng.normal(scale=0.01, size=n)])
    target = (3 * base + rng.normal(scale=0.5, size=n)).reshape(-1, 1)

    def train_ridge(lam, epochs=300, lr=0.05):
        weight, bias = np.zeros((1, 2)), np.zeros(1)
        for _ in range(epochs):
            grad_weight, grad_bias = ridge_grad(input, weight, bias, target, lam)
            weight, bias = gd_step(weight, bias, grad_weight, grad_bias, lr)
        return weight

    assert np.linalg.norm(train_ridge(lam=5.0)) < np.linalg.norm(train_ridge(lam=0.01))
