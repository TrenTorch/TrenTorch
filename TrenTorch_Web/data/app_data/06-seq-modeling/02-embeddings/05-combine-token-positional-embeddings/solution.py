import numpy as np


def combine_embeddings(token_embeddings: np.ndarray, positional_embeddings: np.ndarray) -> np.ndarray:
    return token_embeddings + positional_embeddings
