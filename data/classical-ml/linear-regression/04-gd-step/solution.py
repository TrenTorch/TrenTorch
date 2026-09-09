import numpy as np


def gd_step(w: np.ndarray, b: float, dw: np.ndarray, db: float, lr: float) -> tuple[np.ndarray, float]:
    return w - lr * dw, b - lr * db
