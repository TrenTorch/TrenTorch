"""
pytest data/app_data/01-classical-ml/01-linear-regression/05-training-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

train_linear_regression = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).train_linear_regression
mse_loss = load_solution("01-classical-ml/01-linear-regression/02-mse-loss").mse_loss
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def test_loss_decreases_from_start_to_end():
    rng = np.random.default_rng(4)
    input = rng.normal(size=(100, 3))
    target = input @ np.array([1.0, -2.0, 0.5]) + 3.0 + rng.normal(scale=0.1, size=100)
    initial_prediction = linear(input, np.zeros((1, 3)), np.zeros(1))
    initial_loss = mse_loss(initial_prediction, target.reshape(-1, 1))
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=200)
    final_loss = mse_loss(linear(input, weight, bias), target.reshape(-1, 1))
    assert final_loss < initial_loss


def test_recovers_approximately_correct_parameters():
    rng = np.random.default_rng(5)
    input = rng.normal(size=(300, 2))
    true_weight, true_bias = np.array([3.0, -4.0]), 1.5
    target = input @ true_weight + true_bias + rng.normal(scale=0.05, size=300)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=500)
    assert np.allclose(weight[0], true_weight, atol=0.2)
    assert np.isclose(bias[0], true_bias, atol=0.2)


def test_output_shapes_are_correct():
    # weight/bias must come out in the same (1, in_features) / (1,)
    # shape 01-hypothesis-function's linear expects, never squeezed.
    input, target = np.random.randn(10, 4), np.random.randn(10)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=5)
    assert weight.shape == (1, 4)
    assert bias.shape == (1,)


def test_zero_epochs_returns_initial_parameters():
    input, target = np.random.randn(10, 2), np.random.randn(10)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=0)
    assert np.allclose(weight, np.zeros((1, 2)))
    assert np.allclose(bias, np.zeros(1))


def test_single_feature_dataset():
    rng = np.random.default_rng(6)
    input = rng.normal(size=(200, 1))
    target = 5 * input[:, 0] - 2 + rng.normal(scale=0.05, size=200)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=300)
    assert np.isclose(weight[0, 0], 5.0, atol=0.2)
    assert np.isclose(bias[0], -2.0, atol=0.2)


def test_more_epochs_never_makes_final_loss_worse():
    # Not strictly monotonic every single step (full-batch GD can wobble
    # slightly with a less-than-tiny lr), but running substantially more
    # epochs should not leave us worse off than fewer epochs on the same
    # well-conditioned problem.
    rng = np.random.default_rng(7)
    input = rng.normal(size=(150, 2))
    target = input @ np.array([1.0, 1.0]) + rng.normal(scale=0.05, size=150)
    weight_short, bias_short = train_linear_regression(input, target, lr=0.05, epochs=20)
    weight_long, bias_long = train_linear_regression(input, target, lr=0.05, epochs=400)
    target_2d = target.reshape(-1, 1)
    loss_short = mse_loss(linear(input, weight_short, bias_short), target_2d)
    loss_long = mse_loss(linear(input, weight_long, bias_long), target_2d)
    assert loss_long <= loss_short
