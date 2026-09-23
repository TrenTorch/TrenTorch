import numpy as np


def collaborative_scores(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    return U @ V.T
