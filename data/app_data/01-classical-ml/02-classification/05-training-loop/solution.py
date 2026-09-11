import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
bce_grad = load_solution("01-classical-ml/02-classification/03-bce-gradient").bce_grad


def train_logistic_regression(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float]:
    w = np.zeros(X.shape[1])
    b = 0.0
    for _ in range(epochs):
        z = X @ w + b
        p = sigmoid(z)
        dw, db = bce_grad(X, p, y)
        w = w - lr * dw
        b = b - lr * db
    return w, b
