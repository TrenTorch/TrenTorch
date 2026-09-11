"""
pytest data/01-classical-ml/02-classification/06-softmax-cce/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_this = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}")
softmax = _this.softmax
cce_loss = _this.cce_loss

sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
bce_loss = load_solution("01-classical-ml/02-classification/02-bce-loss").bce_loss


def test_softmax_rows_sum_to_one():
    Z = np.random.default_rng(7).normal(size=(5, 4))
    assert np.allclose(softmax(Z).sum(axis=1), 1.0)


def test_softmax_stable_on_large_logits():
    Z = np.array([[1000.0, 1.0, 0.0]])
    result = softmax(Z)
    assert np.all(np.isfinite(result))
    assert np.isclose(result[0, 0], 1.0, atol=1e-6)


def test_cce_matches_hand_worked_example():
    P = np.array([[0.7, 0.2, 0.1]])
    y = np.array([0])
    assert np.isclose(cce_loss(P, y), -np.log(0.7))


def test_two_class_softmax_cce_matches_sigmoid_bce():
    rng = np.random.default_rng(8)
    z = rng.normal(size=20)
    y = rng.integers(0, 2, 20)
    Z = np.stack([np.zeros(20), z], axis=1)  # class 1 logit = z, class 0 logit = 0
    softmax_loss = cce_loss(softmax(Z), y)
    p = sigmoid(z)
    bce = bce_loss(p, y.astype(float))
    assert np.isclose(softmax_loss, bce, atol=1e-6)


def test_indexing_pulls_correct_column_per_row_not_all_rows():
    # Regression guard: P[:, y_indices] (wrong) vs P[arange(n), y_indices]
    # (right) agree by coincidence on some inputs but not this one.
    P = np.array([[0.9, 0.1], [0.2, 0.8], [0.5, 0.5]])
    y = np.array([0, 1, 0])
    assert np.allclose(cce_loss(P, y), -np.mean(np.log([0.9, 0.8, 0.5])))
