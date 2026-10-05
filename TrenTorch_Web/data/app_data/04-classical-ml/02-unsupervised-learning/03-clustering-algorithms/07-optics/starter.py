import numpy as np


def optics(X: np.ndarray, min_samples: int, max_eps: float = np.inf):
    """
    OPTICS ordering. Returns (ordering, reachability) where ordering is the
    visit order of point indices and reachability[i] is the reachability
    distance of point i (inf when undefined). Raises ValueError when
    min_samples is outside 1..n.
    """
    pass
