import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_grad = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_grad


def ridge_grad(
    X: np.ndarray, y_hat: np.ndarray, y: np.ndarray, w: np.ndarray, lam: float
) -> tuple[np.ndarray, float]:
    dw, db = mse_grad(X, y_hat, y)
    return dw + 2 * lam * w, db
