import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear_forward = load_solution("03-dl-training/02-layers/01-linear-forward").linear_forward
linear_backward = load_solution("03-dl-training/02-layers/02-linear-backward").linear_backward


def mse_loss_and_grad(pred: np.ndarray, target: np.ndarray) -> tuple[float, np.ndarray]:
    """
    Mean squared error and its gradient with respect to `pred`, in one
    call (avoiding a second pass over the data to compute the gradient
    separately).
    """
    pass


def train_one_epoch(
    loader, weight: np.ndarray, bias: np.ndarray, lr: float
) -> tuple[np.ndarray, np.ndarray, float]:
    """
    The five-step loop every PyTorch training script repeats once per
    batch, run here for one full epoch (one full pass over `loader`):
    get a batch of data, run the forward pass, compute the loss (and its
    gradient), backpropagate to get parameter gradients, and take an
    optimizer step. Returns the UPDATED (weight, bias) and the average
    loss across all batches in the epoch.
    """
    pass
