"""
pytest data/app_data/03-dl-training/03-training-loop/02-assemble-training-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/03-training-loop/{Path(__file__).resolve().parent.name}")
mse_loss_and_grad = _module.mse_loss_and_grad
train_one_epoch = _module.train_one_epoch

DL = load_solution("03-dl-training/03-training-loop/01-dataset-dataloader")
ArrayDataset = DL.ArrayDataset
DataLoader = DL.DataLoader


def test_mse_loss_matches_hand_computation():
    pred = np.array([[1.0], [2.0]])
    target = np.array([[0.0], [0.0]])
    loss, _ = mse_loss_and_grad(pred, target)
    # mean of [1, 4] = 2.5
    assert np.isclose(loss, 2.5)


def test_mse_grad_matches_hand_computation():
    pred = np.array([[3.0], [5.0]])
    target = np.array([[1.0], [1.0]])
    _, grad = mse_loss_and_grad(pred, target)
    # grad = 2*(pred-target)/n, n=2: [2*2/2, 2*4/2] = [2, 4]
    assert np.allclose(grad, [[2.0], [4.0]])


def test_mse_loss_is_zero_when_prediction_matches_target_exactly():
    pred = np.array([[1.0, 2.0], [3.0, 4.0]])
    loss, grad = mse_loss_and_grad(pred, pred.copy())
    assert np.isclose(loss, 0.0)
    assert np.allclose(grad, 0.0)


def test_train_one_epoch_reduces_loss_compared_to_a_single_batch_step():
    np.random.seed(0)
    X = np.random.randn(40, 2)
    true_w = np.array([[3.0, -2.0]])
    true_b = np.array([0.5])
    y = X @ true_w.T + true_b

    ds = ArrayDataset(X, y)
    loader = DataLoader(ds, batch_size=8, shuffle=False)

    weight = np.zeros((1, 2))
    bias = np.zeros(1)

    _, _, loss_before = train_one_epoch(loader, weight, bias, lr=0.1)
    weight2, bias2, loss_after_more_epochs = None, None, loss_before
    w, b = weight, bias
    for _ in range(50):
        w, b, loss_after_more_epochs = train_one_epoch(loader, w, b, lr=0.1)

    assert loss_after_more_epochs < loss_before


def test_train_one_epoch_converges_to_the_true_linear_relationship():
    np.random.seed(1)
    X = np.random.randn(200, 3)
    true_w = np.array([[2.0, -1.0, 0.5]])
    true_b = np.array([1.0])
    y = X @ true_w.T + true_b

    ds = ArrayDataset(X, y)
    loader = DataLoader(ds, batch_size=20, shuffle=True, seed=1)

    weight = np.zeros((1, 3))
    bias = np.zeros(1)
    loss = None
    for _ in range(300):
        weight, bias, loss = train_one_epoch(loader, weight, bias, lr=0.1)

    assert loss < 1e-6
    assert np.allclose(weight, true_w, atol=1e-3)
    assert np.allclose(bias, true_b, atol=1e-3)


def test_train_one_epoch_updates_weight_after_every_batch_not_once_at_the_end():
    # Directly targets a mutant that accumulates gradients across the
    # whole epoch and updates weight/bias only ONCE, after the loop
    # (full-batch gradient descent instead of mini-batch SGD): with a
    # large enough learning rate and enough batches, per-batch updates
    # converge dramatically faster within a single call to
    # train_one_epoch than a single accumulated update would.
    np.random.seed(2)
    X = np.random.randn(100, 1)
    true_w = np.array([[4.0]])
    true_b = np.array([0.0])
    y = X @ true_w.T + true_b

    ds = ArrayDataset(X, y)
    loader = DataLoader(ds, batch_size=5, shuffle=False)

    weight = np.zeros((1, 1))
    bias = np.zeros(1)
    weight, bias, loss = train_one_epoch(loader, weight, bias, lr=0.5)
    # per-batch SGD with 20 batches and lr=0.5 makes rapid progress
    # within a SINGLE epoch; a single accumulated full-batch update
    # would leave the weight much further from true_w after one epoch.
    assert abs(weight[0, 0] - 4.0) < 1.0


def test_average_loss_is_the_mean_of_per_batch_losses():
    np.random.seed(3)
    X = np.random.randn(20, 1)
    y = X * 2.0
    ds = ArrayDataset(X, y)
    loader = DataLoader(ds, batch_size=4, shuffle=False)
    weight = np.array([[2.0]])
    bias = np.array([0.0])
    # weight already matches the true relationship exactly, so every
    # batch's own loss should be 0, and so should the average.
    _, _, avg_loss = train_one_epoch(loader, weight, bias, lr=0.0)
    assert np.isclose(avg_loss, 0.0)
