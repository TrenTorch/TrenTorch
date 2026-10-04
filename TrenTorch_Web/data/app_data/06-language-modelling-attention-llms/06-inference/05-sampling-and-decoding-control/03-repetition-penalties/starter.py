import numpy as np


def apply_penalties(logits: np.ndarray, generated_ids: list[int], rep: float = 1.0, freq: float = 0.0, pres: float = 0.0) -> np.ndarray:
    """Return logits with repetition, frequency and presence penalties applied."""
    # TODO
    pass
