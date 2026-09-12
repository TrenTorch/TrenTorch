import numpy as np


def _log_softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    return shifted - np.log(np.sum(np.exp(shifted), axis=-1, keepdims=True))


def cross_entropy_forward(logits: np.ndarray, target: np.ndarray, reduction: str = "mean"):
    n = logits.shape[0]
    log_probs = _log_softmax(logits)
    nll = -log_probs[np.arange(n), target]
    if reduction == "none":
        return nll
    if reduction == "sum":
        return nll.sum()
    return nll.mean()


def cross_entropy_backward(
    logits: np.ndarray, target: np.ndarray, reduction: str = "mean", grad_output=1.0
) -> np.ndarray:
    n = logits.shape[0]
    log_probs = _log_softmax(logits)
    probs = np.exp(log_probs)
    grad = probs.copy()
    grad[np.arange(n), target] -= 1.0
    if reduction == "mean":
        grad = grad / n
    return grad_output * grad
