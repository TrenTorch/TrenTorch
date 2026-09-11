"""
pytest data/01-classical-ml/01-linear-regression/05-training-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

train_linear_regression = load_solution(f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}").train_linear_regression
linear_forward = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear_forward
mse_loss = load_solution("01-classical-ml/01-linear-regression/02-mse-loss").mse_loss


def test_loss_decreases_from_start_to_end():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(100, 3))
    y = X @ np.array([1.0, -2.0, 0.5]) + 3.0 + rng.normal(scale=0.1, size=100)
    initial_loss = mse_loss(linear_forward(X, np.zeros(3), 0.0), y)
    w, b = train_linear_regression(X, y, lr=0.1, epochs=200)
    assert mse_loss(linear_forward(X, w, b), y) < initial_loss


def test_recovers_approximately_correct_parameters():
    rng = np.random.default_rng(5)
    X = rng.normal(size=(300, 2))
    true_w, true_b = np.array([3.0, -4.0]), 1.5
    y = X @ true_w + true_b + rng.normal(scale=0.05, size=300)
    w, b = train_linear_regression(X, y, lr=0.1, epochs=500)
    assert np.allclose(w, true_w, atol=0.2)
    assert np.isclose(b, true_b, atol=0.2)


def test_zero_epochs_returns_initial_parameters():
    X, y = np.random.randn(10, 2), np.random.randn(10)
    w, b = train_linear_regression(X, y, lr=0.1, epochs=0)
    assert np.allclose(w, np.zeros(2)) and b == 0.0


def test_single_feature_dataset():
    rng = np.random.default_rng(6)
    X = rng.normal(size=(200, 1))
    y = 5 * X[:, 0] - 2 + rng.normal(scale=0.05, size=200)
    w, b = train_linear_regression(X, y, lr=0.1, epochs=300)
    assert np.isclose(w[0], 5.0, atol=0.2) and np.isclose(b, -2.0, atol=0.2)


def test_more_epochs_never_makes_final_loss_worse():
    # Not strictly monotonic every single step (full-batch GD can wobble
    # slightly with a less-than-tiny lr), but running substantially more
    # epochs should not leave us worse off than fewer epochs on the same
    # well-conditioned problem.
    rng = np.random.default_rng(7)
    X = rng.normal(size=(150, 2))
    y = X @ np.array([1.0, 1.0]) + rng.normal(scale=0.05, size=150)
    w_short, b_short = train_linear_regression(X, y, lr=0.05, epochs=20)
    w_long, b_long = train_linear_regression(X, y, lr=0.05, epochs=400)
    loss_short = mse_loss(linear_forward(X, w_short, b_short), y)
    loss_long = mse_loss(linear_forward(X, w_long, b_long), y)
    assert loss_long <= loss_short
