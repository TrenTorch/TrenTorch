"""
pytest data/classical-ml/linear-regression/01-hypothesis-function/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _load import load_solution  # noqa: E402

linear_forward = load_solution(Path(__file__).resolve().parent.name).linear_forward


def test_single_feature_matches_hand_computation():
    # Simplest possible case: one feature, one sample.
    # y_hat = 2*3 + 1 = 7 -- catches basic wiring bugs before anything else.
    X = np.array([[3.0]])
    w = np.array([2.0])
    b = 1.0
    assert np.allclose(linear_forward(X, w, b), [7.0])


def test_multi_feature_matches_hand_computation():
    # Two features, two samples -- makes sure the matmul axis is right,
    # not just "any number times any number" (a common transpose bug).
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    w = np.array([1.0, 1.0])
    assert np.allclose(linear_forward(X, w, 0.0), [3.0, 7.0])


def test_output_shape_is_one_dimensional():
    # A common bug: returning shape (n_samples, 1) instead of (n_samples,).
    # Looks fine printed, breaks every downstream loss function that
    # assumes a flat vector.
    X = np.random.randn(10, 4)
    result = linear_forward(X, np.random.randn(4), 0.5)
    assert result.shape == (10,)


def test_zero_weights_returns_bias_for_every_sample():
    # Isolates the bias term from the weight term: with w all zero,
    # every prediction must collapse to exactly b regardless of X.
    X = np.random.randn(5, 3)
    result = linear_forward(X, np.zeros(3), 2.5)
    assert np.allclose(result, np.full(5, 2.5))


def test_single_sample_still_works():
    # n_samples = 1 is an easy edge case to break with careless reshaping.
    X = np.array([[1.0, 2.0, 3.0]])
    w = np.array([1.0, 0.0, -1.0])
    assert np.allclose(linear_forward(X, w, 0.0), [-2.0])


def test_large_random_batch_matches_manual_loop():
    # The real correctness bar: compare the vectorized implementation
    # against a naive per-sample Python loop on a large random batch.
    # If they ever disagree, the vectorized version has a bug -- the
    # loop version is slow but effectively impossible to get subtly wrong.
    rng = np.random.default_rng(0)
    X = rng.normal(size=(500, 20))
    w = rng.normal(size=20)
    b = float(rng.normal())
    vectorized = linear_forward(X, w, b)
    manual = np.array([X[i] @ w + b for i in range(X.shape[0])])
    assert np.allclose(vectorized, manual)
