import numpy as np


def dropout_forward(x: np.ndarray, p: float, rng: np.random.Generator) -> np.ndarray:
    mask = (rng.random(x.shape) >= p).astype(x.dtype)
    return x * mask / (1.0 - p)
