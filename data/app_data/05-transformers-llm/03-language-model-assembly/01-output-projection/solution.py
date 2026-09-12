import numpy as np


def output_projection(hidden_states: np.ndarray, output_weight: np.ndarray) -> np.ndarray:
    return hidden_states @ output_weight.T
