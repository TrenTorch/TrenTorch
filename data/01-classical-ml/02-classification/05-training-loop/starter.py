import numpy as np


def train_logistic_regression(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float]:
    """
    Returns final_w, final_b.
    """
    # TODO: Initialize w, b to zero, then repeat for `epochs` iterations:
    #   1. Compute logits z = X @ w + b, then p = sigmoid(z)
    #   2. Compute gradients with bce_grad()
    #   3. Update w, b with a plain gradient-descent step
    # Reuse sigmoid() and bce_grad() -- don't reimplement their logic.
    pass
