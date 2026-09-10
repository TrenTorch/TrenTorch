"""
pytest data/01-classical-ml/01-linear-regression/03-mse-gradient/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_grad = load_solution(f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}").mse_grad
linear_forward = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear_forward
mse_loss = load_solution("01-classical-ml/01-linear-regression/02-mse-loss").mse_loss
# Forward reference on purpose: this track's last test checks that
# mse_grad's sign convention actually cooperates with gd_step's update
# direction (Q4) -- the two only mean anything together.
gd_step = load_solution("01-classical-ml/01-linear-regression/04-gd-step").gd_step


def test_shapes_are_correct():
    X = np.random.randn(10, 4)
    dw, db = mse_grad(X, np.random.randn(10), np.random.randn(10))
    assert dw.shape == (4,)
    assert np.isscalar(db) or isinstance(db, float)


def test_zero_gradient_at_perfect_predictions():
    # If y_hat == y exactly, the loss is already at its minimum --
    # gradient descent must not move at all from a perfect solution.
    X = np.random.randn(6, 3)
    y = np.random.randn(6)
    dw, db = mse_grad(X, y, y)
    assert np.allclose(dw, 0.0)
    assert np.isclose(db, 0.0)


def test_matches_finite_difference_gradient():
    # The real correctness bar: perturb w/b by a tiny amount and confirm
    # the measured change in loss matches the analytical gradient's
    # prediction. Catches sign errors and missing factors of 2/n that a
    # single hardcoded-example test would miss entirely.
    rng = np.random.default_rng(1)
    X = rng.normal(size=(20, 3))
    w = rng.normal(size=3)
    b = float(rng.normal())
    y = rng.normal(size=20)
    dw, db = mse_grad(X, linear_forward(X, w, b), y)

    eps = 1e-6
    for j in range(3):
        w_plus, w_minus = w.copy(), w.copy()
        w_plus[j] += eps
        w_minus[j] -= eps
        numerical = (mse_loss(linear_forward(X, w_plus, b), y)
                     - mse_loss(linear_forward(X, w_minus, b), y)) / (2 * eps)
        assert np.isclose(dw[j], numerical, atol=1e-4)

    numerical_db = (mse_loss(linear_forward(X, w, b + eps), y)
                    - mse_loss(linear_forward(X, w, b - eps), y)) / (2 * eps)
    assert np.isclose(db, numerical_db, atol=1e-4)


def test_gradient_direction_actually_reduces_loss():
    # This is really a sign-convention test: stepping opposite the
    # gradient (an actual GD step) must decrease loss, not increase it.
    rng = np.random.default_rng(2)
    X = rng.normal(size=(30, 2))
    w = rng.normal(size=2)
    y = rng.normal(size=30)
    y_hat = linear_forward(X, w, 0.0)
    dw, db = mse_grad(X, y_hat, y)
    loss_before = mse_loss(y_hat, y)
    w_new, b_new = gd_step(w, 0.0, dw, db, lr=0.01)
    assert mse_loss(linear_forward(X, w_new, b_new), y) < loss_before
