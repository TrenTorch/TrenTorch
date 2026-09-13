"""
pytest data/app_data/01-classical-ml/01-linear-regression/05-training-loop/tests.py

Numbered for the same reason every question in this track is: "Run"
shows the first couple by name, "Submit" runs all of them, and the
numbering keeps both views in the same deliberate order (basic
correctness, recovery/shape/edge-case coverage, then a real torch
oracle over an identical full-batch run).
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


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_loss_decreases_from_start_to_end():
    rng = np.random.default_rng(4)
    input = rng.normal(size=(100, 3))
    target = input @ np.array([1.0, -2.0, 0.5]) + 3.0 + rng.normal(scale=0.1, size=100)
    initial_prediction = linear(input, np.zeros((1, 3)), np.zeros(1))
    initial_loss = mse_loss(initial_prediction, target.reshape(-1, 1))
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=200)
    final_loss = mse_loss(linear(input, weight, bias), target.reshape(-1, 1))
    assert final_loss < initial_loss


def test_02_recovers_approximately_correct_parameters():
    rng = np.random.default_rng(5)
    input = rng.normal(size=(300, 2))
    true_weight, true_bias = np.array([3.0, -4.0]), 1.5
    target = input @ true_weight + true_bias + rng.normal(scale=0.05, size=300)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=500)
    assert np.allclose(weight[0], true_weight, atol=0.2)
    assert np.isclose(bias[0], true_bias, atol=0.2)


# --- Shape handling ---------------------------------------------------


def test_03_output_shapes_are_correct():
    # weight/bias must come out in the same (1, in_features) / (1,)
    # shape 01-hypothesis-function's linear expects, never squeezed.
    input, target = np.random.randn(10, 4), np.random.randn(10)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=5)
    assert weight.shape == (1, 4)
    assert bias.shape == (1,)


# --- Edge cases -------------------------------------------------------


def test_04_zero_epochs_returns_initial_parameters():
    input, target = np.random.randn(10, 2), np.random.randn(10)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=0)
    assert np.allclose(weight, np.zeros((1, 2)))
    assert np.allclose(bias, np.zeros(1))


def test_05_single_feature_dataset():
    rng = np.random.default_rng(6)
    input = rng.normal(size=(200, 1))
    target = 5 * input[:, 0] - 2 + rng.normal(scale=0.05, size=200)
    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=300)
    assert np.isclose(weight[0, 0], 5.0, atol=0.2)
    assert np.isclose(bias[0], -2.0, atol=0.2)


def test_06_more_epochs_never_makes_final_loss_worse():
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


# --- Independent correctness oracle -----------------------------------


def test_07_matches_real_pytorch_on_identical_full_batch_run():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   torch.manual_seed(0)
    #   X = torch.randn(20, 2, dtype=torch.float32)
    #   true_w = torch.tensor([1.5, -2.0])
    #   y = X @ true_w + 0.5 + 0.01 * torch.randn(20)
    #   model = torch.nn.Linear(2, 1)
    #   with torch.no_grad(): model.weight.zero_(); model.bias.zero_()
    #   optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    #   loss_fn = torch.nn.MSELoss()
    #   for _ in range(50):
    #       optimizer.zero_grad()
    #       loss = loss_fn(model(X).squeeze(-1), y)
    #       loss.backward()
    #       optimizer.step()
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    input = np.array(
        [
            [-1.1258398, -1.1523602],
            [-0.25057858, -0.43387881],
            [0.84871036, 0.69200915],
            [-0.31601277, -2.11521935],
            [0.32227492, -1.26333475],
            [0.34998319, 0.30813393],
            [0.11984151, 1.2376579],
            [1.11677718, -0.24727815],
            [-1.35265374, -1.6959312],
            [0.56665063, 0.79350835],
            [0.59883946, -1.55509508],
            [-0.34136039, 1.85300612],
            [-0.21586326, -0.74254817],
            [0.56272137, 0.2596274],
            [-0.173961, -0.67874622],
            [0.93826073, 0.48886982],
            [1.20322371, 0.0845347],
            [-1.2001394, -0.00478574],
            [-0.51807481, -0.30670419],
            [-1.58099389, 1.70664334],
        ],
        dtype=np.float32,
    )
    target = np.array(
        [
            1.11801589, 0.98738641, 0.38331649, 4.25086594, 3.49882579, 0.40553692,
            -1.80647814, 2.66887021, 1.86194813, -0.23017025, 4.50006628, -3.71804404,
            1.65379715, 0.82668132, 1.60276234, 0.93603325, 2.13330603, -1.26761246,
            0.31747925, -5.28527498,
        ],
        dtype=np.float32,
    )
    expected_weight = np.array([[1.4961023, -1.99810839]], dtype=np.float32)
    expected_bias = np.array([0.49848327], dtype=np.float32)

    weight, bias = train_linear_regression(input, target, lr=0.1, epochs=50)
    assert np.allclose(weight, expected_weight, atol=1e-3)
    assert np.allclose(bias, expected_bias, atol=1e-3)
