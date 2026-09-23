import numpy as np


def predict_labels(p: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    return (p >= threshold).astype(int)
