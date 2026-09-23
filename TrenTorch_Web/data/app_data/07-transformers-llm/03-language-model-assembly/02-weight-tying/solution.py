import numpy as np


def compute_output_logits(
    hidden_states: np.ndarray,
    embedding_table: np.ndarray,
    tied: bool,
    output_weight: np.ndarray | None = None,
) -> np.ndarray:
    matrix = embedding_table if tied else output_weight
    return hidden_states @ matrix.T


def count_output_head_parameters(vocab_size: int, d_model: int, tied: bool) -> int:
    if tied:
        return 0
    return vocab_size * d_model
