import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear_forward = load_solution("03-dl-training/02-layers/01-linear-forward").linear_forward
linear_backward = load_solution("03-dl-training/02-layers/02-linear-backward").linear_backward


def mse_loss_and_grad(pred: np.ndarray, target: np.ndarray) -> tuple[float, np.ndarray]:
    loss = float(np.mean((pred - target) ** 2))
    grad_pred = 2.0 * (pred - target) / pred.size
    return loss, grad_pred


def train_one_epoch(
    loader, weight: np.ndarray, bias: np.ndarray, lr: float
) -> tuple[np.ndarray, np.ndarray, float]:
    total_loss = 0.0
    n_batches = 0

    for batch_x, batch_y in loader:
        pred = linear_forward(batch_x, weight, bias)
        loss, grad_pred = mse_loss_and_grad(pred, batch_y)
        _, grad_weight, grad_bias = linear_backward(grad_pred, batch_x, weight)

        weight = weight - lr * grad_weight
        bias = bias - lr * grad_bias

        total_loss += loss
        n_batches += 1

    return weight, bias, total_loss / n_batches
