import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_grad = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_grad
gd_step = load_solution("01-classical-ml/01-linear-regression/04-gd-step").gd_step

# Temporary shim: 01-hypothesis-function now implements the general
# torch.nn.functional.linear signature (2D weight, optional bias, 2D
# output) -- adapt back to this track's 1D-weight/scalar-bias/1D-output
# convention until this question gets its own PyTorch-style pass too.
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def linear_forward(X, w, b):
    return linear(X, w.reshape(1, -1), np.array([b])).reshape(-1)


def train_linear_regression(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float]:
    w = np.zeros(X.shape[1])
    b = 0.0
    for _ in range(epochs):
        y_hat = linear_forward(X, w, b)
        dw, db = mse_grad(X, y_hat, y)
        w, b = gd_step(w, b, dw, db, lr)
    return w, b
