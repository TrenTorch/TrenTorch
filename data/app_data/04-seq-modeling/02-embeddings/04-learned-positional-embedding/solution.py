import numpy as np


def learned_positional_embedding(seq_len: int, position_table: np.ndarray) -> np.ndarray:
    return position_table[:seq_len]
