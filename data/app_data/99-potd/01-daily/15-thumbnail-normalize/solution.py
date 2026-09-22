import numpy as np


def normalize_image(matrix: np.ndarray) -> tuple[float, float, np.ndarray]:
    mu = float(matrix.mean())
    sigma = float(matrix.std())  # ddof=0: population standard deviation

    if sigma == 0.0:
        normalized = np.zeros_like(matrix, dtype=float)
    else:
        normalized = (matrix - mu) / sigma

    return mu, sigma, normalized
