import numpy as np


def scale_logits_before_softmax(logits: np.ndarray, d_model: int) -> np.ndarray:
    return logits / np.sqrt(d_model)
