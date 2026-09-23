import numpy as np


def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    norm_u = float(np.linalg.norm(u))
    norm_v = float(np.linalg.norm(v))

    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0

    dot = float(u @ v)
    return dot / (norm_u * norm_v)
