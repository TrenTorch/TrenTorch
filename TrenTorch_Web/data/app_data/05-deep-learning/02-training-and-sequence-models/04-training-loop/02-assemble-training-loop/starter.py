
import numpy as np

from _load import load_solution

linear_forward = load_solution("dl-training-linear-forward").linear_forward
linear_backward = load_solution("dl-training-linear-backward").linear_backward


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
