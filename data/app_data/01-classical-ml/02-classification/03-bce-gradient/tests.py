"""
pytest data/app_data/01-classical-ml/02-classification/03-bce-gradient/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

bce_gradient = load_solution(
    f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}"
).bce_gradient
bce_loss = load_solution("01-classical-ml/02-classification/02-bce-loss").bce_loss


def test_shapes():
    input = np.random.randn(10, 4)
    p = np.random.rand(10, 1)
    target = np.random.randint(0, 2, (10, 1)).astype(float)
    grad_weight, grad_bias = bce_gradient(input, p, target)
    assert grad_weight.shape == (1, 4)
    assert grad_bias.shape == (1,)


def test_zero_gradient_at_perfect_confident_prediction():
    input = np.random.randn(5, 2)
    target = np.array([[1.0], [0.0], [1.0], [0.0], [1.0]])
    p = target.copy()  # perfect prediction
    grad_weight, grad_bias = bce_gradient(input, p, target)
    assert np.allclose(grad_weight, 0.0)
    assert np.allclose(grad_bias, 0.0)


def test_matches_finite_difference_of_bce():
    rng = np.random.default_rng(2)
    input = rng.normal(size=(30, 3))
    weight = rng.normal(size=(1, 3))
    bias = np.array([float(rng.normal())])
    target = rng.integers(0, 2, (30, 1)).astype(float)

    def loss_at(weight_, bias_):
        z = input @ weight_.T + bias_
        p_ = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        return bce_loss(p_, target)

    z = input @ weight.T + bias
    p = 1 / (1 + np.exp(-z))
    grad_weight, grad_bias = bce_gradient(input, p, target)

    eps = 1e-6
    for j in range(3):
        weight_plus, weight_minus = weight.copy(), weight.copy()
        weight_plus[0, j] += eps
        weight_minus[0, j] -= eps
        numerical = (loss_at(weight_plus, bias) - loss_at(weight_minus, bias)) / (2 * eps)
        assert np.isclose(grad_weight[0, j], numerical, atol=1e-4)

    numerical_bias = (loss_at(weight, bias + eps) - loss_at(weight, bias - eps)) / (2 * eps)
    assert np.isclose(grad_bias[0], numerical_bias, atol=1e-4)


def test_gradient_scale_is_1_over_n_not_2_over_n():
    # Regression guard against copy-pasting Linear Regression's factor
    # of 2 -- doubling n_samples via exact duplication of every row
    # must leave the *mean* gradient unchanged.
    rng = np.random.default_rng(3)
    input = rng.normal(size=(20, 2))
    target = rng.integers(0, 2, (20, 1)).astype(float)
    p = rng.random((20, 1))
    grad_weight1, grad_bias1 = bce_gradient(input, p, target)
    input2 = np.vstack([input, input])
    p2 = np.vstack([p, p])
    target2 = np.vstack([target, target])
    grad_weight2, grad_bias2 = bce_gradient(input2, p2, target2)
    assert np.allclose(grad_weight1, grad_weight2, atol=1e-8)
    assert np.allclose(grad_bias1, grad_bias2, atol=1e-8)
