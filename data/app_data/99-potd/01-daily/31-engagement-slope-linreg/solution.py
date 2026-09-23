import numpy as np


def fit_line(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    mean_x = float(np.mean(x))
    mean_y = float(np.mean(y))

    dx = x - mean_x
    dy = y - mean_y
    denominator = float(np.sum(dx**2))

    if denominator == 0.0:
        return 0.0, mean_y

    w = float(np.sum(dx * dy)) / denominator
    b = mean_y - w * mean_x
    return w, b
