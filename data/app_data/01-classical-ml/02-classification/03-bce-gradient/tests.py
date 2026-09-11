"""
pytest data/01-classical-ml/02-classification/03-bce-gradient/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

bce_grad = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").bce_grad
bce_loss = load_solution("01-classical-ml/02-classification/02-bce-loss").bce_loss


def test_shapes():
    X = np.random.randn(10, 4)
    dw, db = bce_grad(X, np.random.rand(10), np.random.randint(0, 2, 10).astype(float))
    assert dw.shape == (4,)
    assert isinstance(db, float)


def test_zero_gradient_at_perfect_confident_prediction():
    X = np.random.randn(5, 2)
    y = np.array([1.0, 0.0, 1.0, 0.0, 1.0])
    p = y.copy()  # perfect prediction
    dw, db = bce_grad(X, p, y)
    assert np.allclose(dw, 0.0) and np.isclose(db, 0.0)


def test_matches_finite_difference_of_bce():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(30, 3))
    w = rng.normal(size=3)
    b = float(rng.normal())
    y = rng.integers(0, 2, 30).astype(float)

    def loss_at(w_, b_):
        z = X @ w_ + b_
        p = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        return bce_loss(p, y)

    z = X @ w + b
    p = 1 / (1 + np.exp(-z))
    dw, db = bce_grad(X, p, y)

    eps = 1e-6
    for j in range(3):
        wp, wm = w.copy(), w.copy()
        wp[j] += eps
        wm[j] -= eps
        numerical = (loss_at(wp, b) - loss_at(wm, b)) / (2 * eps)
        assert np.isclose(dw[j], numerical, atol=1e-4)


def test_gradient_scale_is_1_over_n_not_2_over_n():
    # Regression guard against copy-pasting Linear Regression's factor
    # of 2 -- doubling n_samples via exact duplication of every row
    # must leave the *mean* gradient unchanged.
    rng = np.random.default_rng(3)
    X = rng.normal(size=(20, 2))
    y = rng.integers(0, 2, 20).astype(float)
    p = rng.random(20)
    dw1, db1 = bce_grad(X, p, y)
    X2 = np.vstack([X, X])
    p2 = np.concatenate([p, p])
    y2 = np.concatenate([y, y])
    dw2, db2 = bce_grad(X2, p2, y2)
    assert np.allclose(dw1, dw2, atol=1e-8)
    assert np.isclose(db1, db2, atol=1e-8)
