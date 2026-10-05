import numpy as np


def soft_threshold(z: np.ndarray, t: float) -> np.ndarray:
    """Elementwise soft threshold: sign(z) * max(|z| - t, 0)."""
    pass


def sparse_code(D: np.ndarray, y: np.ndarray, lam: float = 0.1, iters: int = 100) -> np.ndarray:
    """
    ISTA for min 0.5 * ||y - D x||^2 + lam * ||x||_1, starting from x = 0.
    Step size is 1 / ||D||_2^2 (or 1.0 if that is zero). Raises ValueError for
    shape mismatch, negative lam, or negative iters.
    """
    pass
