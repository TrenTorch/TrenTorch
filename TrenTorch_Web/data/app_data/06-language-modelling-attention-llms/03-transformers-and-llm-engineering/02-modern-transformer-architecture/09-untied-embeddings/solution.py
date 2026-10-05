import numpy as np


def output_projection_tied(hidden_states: np.ndarray, embedding_table: np.ndarray) -> np.ndarray:
    return hidden_states @ embedding_table.T


def output_projection_untied(hidden_states: np.ndarray, output_weight: np.ndarray) -> np.ndarray:
    return hidden_states @ output_weight.T
