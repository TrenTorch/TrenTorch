"""
pytest data/app_data/01-classical-ml/02-classification/05-training-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

train_logistic_regression = load_solution(
    f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}"
).train_logistic_regression
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
bce_loss = load_solution("01-classical-ml/02-classification/02-bce-loss").bce_loss
predict_labels = load_solution("01-classical-ml/02-classification/04-decision-boundary").predict_labels


def test_loss_decreases():
    rng = np.random.default_rng(4)
    input = rng.normal(size=(200, 2))
    true_weight = np.array([2.0, -1.5])
    target = (1 / (1 + np.exp(-(input @ true_weight))) > 0.5).astype(float)
    initial_prediction = sigmoid(linear(input, np.zeros((1, 2)), np.zeros(1)))
    initial_loss = bce_loss(initial_prediction, target.reshape(-1, 1))
    weight, bias = train_logistic_regression(input, target, lr=0.5, epochs=300)
    final_loss = bce_loss(sigmoid(linear(input, weight, bias)), target.reshape(-1, 1))
    assert final_loss < initial_loss


def test_output_shapes_are_correct():
    input, target = np.random.randn(10, 4), np.random.randint(0, 2, 10).astype(float)
    weight, bias = train_logistic_regression(input, target, lr=0.1, epochs=5)
    assert weight.shape == (1, 4)
    assert bias.shape == (1,)


def test_separates_linearly_separable_data():
    rng = np.random.default_rng(5)
    input_pos = rng.normal(loc=2.0, size=(50, 2))
    input_neg = rng.normal(loc=-2.0, size=(50, 2))
    input = np.vstack([input_pos, input_neg])
    target = np.concatenate([np.ones(50), np.zeros(50)])
    weight, bias = train_logistic_regression(input, target, lr=0.1, epochs=500)
    predictions = predict_labels(sigmoid(linear(input, weight, bias)))
    accuracy = np.mean(predictions.reshape(-1) == target)
    assert accuracy > 0.95


def test_zero_epochs_stays_at_init():
    input, target = np.random.randn(10, 2), np.random.randint(0, 2, 10).astype(float)
    weight, bias = train_logistic_regression(input, target, lr=0.1, epochs=0)
    assert np.allclose(weight, 0.0)
    assert np.allclose(bias, 0.0)


def test_single_feature():
    rng = np.random.default_rng(6)
    x = rng.normal(size=200)
    target = (x > 0).astype(float)
    input = x.reshape(-1, 1)
    weight, bias = train_logistic_regression(input, target, lr=0.3, epochs=400)
    predictions = predict_labels(sigmoid(linear(input, weight, bias)))
    accuracy = np.mean(predictions.reshape(-1) == target)
    assert accuracy > 0.9
