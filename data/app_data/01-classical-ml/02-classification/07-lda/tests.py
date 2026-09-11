"""
pytest data/01-classical-ml/02-classification/07-lda/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

lda_fit = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").lda_fit
sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
train_logistic_regression = load_solution("01-classical-ml/02-classification/05-training-loop").train_logistic_regression
predict_labels = load_solution("01-classical-ml/02-classification/04-decision-boundary").predict_labels


def test_separates_two_shared_covariance_gaussians():
    rng = np.random.default_rng(9)
    cov = np.array([[1.0, 0.3], [0.3, 1.0]])
    X0 = rng.multivariate_normal([0, 0], cov, size=200)
    X1 = rng.multivariate_normal([4, 4], cov, size=200)
    X = np.vstack([X0, X1])
    y = np.concatenate([np.zeros(200), np.ones(200)])
    w, b = lda_fit(X, y)
    preds = (X @ w + b >= 0).astype(int)
    assert np.mean(preds == y) > 0.9


def test_matches_logistic_regression_accuracy_on_gaussian_data():
    rng = np.random.default_rng(10)
    cov = np.eye(2)
    X0 = rng.multivariate_normal([-2, -2], cov, size=150)
    X1 = rng.multivariate_normal([2, 2], cov, size=150)
    X = np.vstack([X0, X1])
    y = np.concatenate([np.zeros(150), np.ones(150)])
    w_lda, b_lda = lda_fit(X, y)
    w_log, b_log = train_logistic_regression(X, y, lr=0.1, epochs=300)
    acc_lda = np.mean((X @ w_lda + b_lda >= 0).astype(int) == y)
    acc_log = np.mean(predict_labels(sigmoid(X @ w_log + b_log)) == y)
    assert abs(acc_lda - acc_log) < 0.05


def test_unequal_class_sizes_shift_boundary_toward_larger_class():
    # With one class much more common, LDA's prior term should make it
    # harder to predict the rare class -- dropping the log-prior term
    # would fail this by treating both priors as equal regardless.
    rng = np.random.default_rng(11)
    cov = np.eye(2) * 4  # wide spread so priors actually matter
    X0 = rng.multivariate_normal([0, 0], cov, size=950)
    X1 = rng.multivariate_normal([2, 2], cov, size=50)
    X = np.vstack([X0, X1])
    y = np.concatenate([np.zeros(950), np.ones(50)])
    w, b = lda_fit(X, y)
    midpoint = np.array([1.0, 1.0])
    score_at_midpoint = midpoint @ w + b
    assert score_at_midpoint < 0  # classified as the majority class


def test_unbiased_covariance_uses_n_minus_2():
    # A hand-checkable case: 3 points per class, verify pooled_cov
    # divides by (n-2)=4, not n=6, by comparing against a manual
    # computation of the same formula. Points need spread in both
    # dimensions -- collinear points along one axis make the pooled
    # covariance singular (zero variance on the other axis), which
    # np.linalg.inv correctly refuses to invert.
    X0 = np.array([[0.0, 0.0], [1.0, 1.0], [-1.0, 1.0]])
    X1 = np.array([[5.0, 0.0], [6.0, 1.0], [4.0, 1.0]])
    X = np.vstack([X0, X1])
    y = np.array([0, 0, 0, 1, 1, 1])
    mu0, mu1 = X0.mean(axis=0), X1.mean(axis=0)
    expected_cov = ((X0 - mu0).T @ (X0 - mu0) + (X1 - mu1).T @ (X1 - mu1)) / 4
    w, _ = lda_fit(X, y)
    expected_w = np.linalg.inv(expected_cov) @ (mu1 - mu0)
    assert np.allclose(w, expected_w)
