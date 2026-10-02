import numpy as np


def is_view_of(candidate: np.ndarray, source: np.ndarray) -> bool:
    return bool(np.shares_memory(candidate, source))
