import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _load import load_solution  # noqa: E402

linear_forward = load_solution("01-hypothesis-function").linear_forward
mse_grad = load_solution("03-mse-gradient").mse_grad
gd_step = load_solution("04-gd-step").gd_step


def train_linear_regression(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float]:
    w = np.zeros(X.shape[1])
    b = 0.0
    for _ in range(epochs):
        y_hat = linear_forward(X, w, b)
        dw, db = mse_grad(X, y_hat, y)
        w, b = gd_step(w, b, dw, db, lr)
    return w, b
