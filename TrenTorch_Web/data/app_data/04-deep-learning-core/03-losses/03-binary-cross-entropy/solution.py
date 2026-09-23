import numpy as np

_EPS = 1e-12


def bce_loss_forward(probs: np.ndarray, target: np.ndarray, reduction: str = "mean"):
    clipped = np.clip(probs, _EPS, 1.0 - _EPS)
    elementwise = -(target * np.log(clipped) + (1.0 - target) * np.log(1.0 - clipped))
    if reduction == "none":
        return elementwise
    if reduction == "sum":
        return elementwise.sum()
    return elementwise.mean()


def bce_loss_backward(
    probs: np.ndarray, target: np.ndarray, reduction: str = "mean", grad_output=1.0
) -> np.ndarray:
    clipped = np.clip(probs, _EPS, 1.0 - _EPS)
    grad = (clipped - target) / (clipped * (1.0 - clipped))
    if reduction == "mean":
        grad = grad / probs.size
    return grad_output * grad
