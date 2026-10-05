import numpy as np


def softmax_probabilities(q_values: np.ndarray, temperature: float) -> np.ndarray:
    logits = np.asarray(q_values, dtype=float) / temperature
    logits = logits - logits.max()
    weights = np.exp(logits)
    return weights / weights.sum()
