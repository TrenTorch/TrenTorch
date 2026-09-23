import numpy as np


def embedding_forward(token_ids: np.ndarray, embedding_table: np.ndarray) -> np.ndarray:
    return embedding_table[token_ids]
