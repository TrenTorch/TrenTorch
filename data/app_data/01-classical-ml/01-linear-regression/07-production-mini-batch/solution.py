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


def train_linear_regression_production(
    X: np.ndarray, y: np.ndarray, lr: float, epochs: int, batch_size: int, seed: int | None = None
) -> tuple[np.ndarray, float]:
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0
    rng = np.random.default_rng(seed)

    for _ in range(epochs):
        order = rng.permutation(n_samples)
        for start in range(0, n_samples, batch_size):
            batch_idx = order[start:start + batch_size]
            X_batch, y_batch = X[batch_idx], y[batch_idx]
            y_hat = linear_forward(X_batch, w, b)
            dw, db = mse_grad(X_batch, y_hat, y_batch)
            w, b = gd_step(w, b, dw, db, lr)

    return w, b
