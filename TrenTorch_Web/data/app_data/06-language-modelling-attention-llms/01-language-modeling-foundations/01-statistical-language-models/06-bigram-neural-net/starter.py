import numpy as np


def _softmax_rows(logits: np.ndarray) -> np.ndarray:
    # TODO (optional helper): numerically stable row-wise softmax.
    pass


def bigram_net_loss(W: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> float:
    """Mean negative log-likelihood of the pairs under softmax(W[x])."""
    # TODO: Look up rows, softmax, take the true column, average -log.
    pass


def bigram_net_gradient(W: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    """Exact gradient of bigram_net_loss with respect to W, shape (V, V)."""
    # TODO: Subtract the one-hot target from the probabilities and scatter-add by row.
    pass


def train_bigram_net(xs: np.ndarray, ys: np.ndarray, V: int, steps: int, lr: float) -> np.ndarray:
    """Plain gradient descent from W = zeros((V, V)); returns the final W."""
    # TODO: Loop `steps` times updating W -= lr * gradient.
    pass
