"""
pytest data/01-classical-ml/02-classification/05-training-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

train_logistic_regression = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").train_logistic_regression
sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
bce_loss = load_solution("01-classical-ml/02-classification/02-bce-loss").bce_loss
predict_labels = load_solution("01-classical-ml/02-classification/04-decision-boundary").predict_labels


def test_loss_decreases():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(200, 2))
    true_w = np.array([2.0, -1.5])
    y = (1 / (1 + np.exp(-(X @ true_w))) > 0.5).astype(float)
    initial_loss = bce_loss(sigmoid(X @ np.zeros(2) + 0.0), y)
    w, b = train_logistic_regression(X, y, lr=0.5, epochs=300)
    final_loss = bce_loss(sigmoid(X @ w + b), y)
    assert final_loss < initial_loss


def test_separates_linearly_separable_data():
    rng = np.random.default_rng(5)
    X_pos = rng.normal(loc=2.0, size=(50, 2))
    X_neg = rng.normal(loc=-2.0, size=(50, 2))
    X = np.vstack([X_pos, X_neg])
    y = np.concatenate([np.ones(50), np.zeros(50)])
    w, b = train_logistic_regression(X, y, lr=0.1, epochs=500)
    preds = predict_labels(sigmoid(X @ w + b))
    accuracy = np.mean(preds == y)
    assert accuracy > 0.95


def test_zero_epochs_stays_at_init():
    X, y = np.random.randn(10, 2), np.random.randint(0, 2, 10).astype(float)
    w, b = train_logistic_regression(X, y, lr=0.1, epochs=0)
    assert np.allclose(w, 0.0) and b == 0.0


def test_single_feature():
    rng = np.random.default_rng(6)
    x = rng.normal(size=200)
    y = (x > 0).astype(float)
    X = x.reshape(-1, 1)
    w, b = train_logistic_regression(X, y, lr=0.3, epochs=400)
    accuracy = np.mean(predict_labels(sigmoid(X @ w + b)) == y)
    assert accuracy > 0.9
