"""
pytest data/classical-ml/linear-regression/06-ridge-regularization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _load import load_solution  # noqa: E402

ridge_grad = load_solution(Path(__file__).resolve().parent.name).ridge_grad
linear_forward = load_solution("01-hypothesis-function").linear_forward
mse_loss = load_solution("02-mse-loss").mse_loss
mse_grad = load_solution("03-mse-gradient").mse_grad
gd_step = load_solution("04-gd-step").gd_step


def test_lambda_zero_matches_plain_mse_gradient():
    rng = np.random.default_rng(7)
    X, w, y = rng.normal(size=(20, 4)), rng.normal(size=4), rng.normal(size=20)
    y_hat = linear_forward(X, w, 0.0)
    dw_plain, db_plain = mse_grad(X, y_hat, y)
    dw_ridge, db_ridge = ridge_grad(X, y_hat, y, w, lam=0.0)
    assert np.allclose(dw_plain, dw_ridge) and np.isclose(db_plain, db_ridge)


def test_bias_gradient_is_never_penalized():
    rng = np.random.default_rng(8)
    X, w, y = rng.normal(size=(15, 3)), rng.normal(size=3), rng.normal(size=15)
    y_hat = linear_forward(X, w, 0.0)
    _, db_plain = mse_grad(X, y_hat, y)
    _, db_ridge = ridge_grad(X, y_hat, y, w, lam=5.0)
    assert np.isclose(db_plain, db_ridge)


def test_matches_finite_difference_of_penalized_loss():
    rng = np.random.default_rng(9)
    X, w, y = rng.normal(size=(20, 3)), rng.normal(size=3), rng.normal(size=20)
    lam = 0.5

    def penalized_loss(w_):
        return mse_loss(linear_forward(X, w_, 0.0), y) + lam * np.sum(w_ ** 2)

    dw, _ = ridge_grad(X, linear_forward(X, w, 0.0), y, w, lam)
    eps = 1e-6
    for j in range(3):
        w_plus, w_minus = w.copy(), w.copy()
        w_plus[j] += eps
        w_minus[j] -= eps
        numerical = (penalized_loss(w_plus) - penalized_loss(w_minus)) / (2 * eps)
        assert np.isclose(dw[j], numerical, atol=1e-4)


def test_larger_lambda_shrinks_weight_norm_after_training():
    # The actual point of ridge, checked end to end: on near-collinear
    # features, a bigger penalty must produce a smaller ||w|| once
    # trained -- not just a bigger number plugged into an untested formula.
    rng = np.random.default_rng(10)
    n = 200
    base = rng.normal(size=n)
    X = np.column_stack([base, base + rng.normal(scale=0.01, size=n)])
    y = 3 * base + rng.normal(scale=0.5, size=n)

    def train_ridge(lam, epochs=300, lr=0.05):
        w, b = np.zeros(2), 0.0
        for _ in range(epochs):
            y_hat = linear_forward(X, w, b)
            dw, db = ridge_grad(X, y_hat, y, w, lam)
            w, b = gd_step(w, b, dw, db, lr)
        return w

    assert np.linalg.norm(train_ridge(lam=5.0)) < np.linalg.norm(train_ridge(lam=0.01))
