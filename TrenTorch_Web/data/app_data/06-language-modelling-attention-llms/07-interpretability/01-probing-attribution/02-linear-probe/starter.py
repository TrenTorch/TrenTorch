import numpy as np


def train_linear_probe(X: np.ndarray, y: np.ndarray, steps: int, lr: float, l2: float):
    """Full-batch gradient descent from zeros; returns (w, b)."""
    # TODO
    pass


def probe_accuracy(X: np.ndarray, y: np.ndarray, w: np.ndarray, b: float) -> float:
    """Fraction of examples with (X @ w + b > 0) == y."""
    # TODO
    pass
