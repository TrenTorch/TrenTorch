import numpy as np


def embedding_lookup(E: np.ndarray, ids: np.ndarray) -> np.ndarray:
    return E[ids]
