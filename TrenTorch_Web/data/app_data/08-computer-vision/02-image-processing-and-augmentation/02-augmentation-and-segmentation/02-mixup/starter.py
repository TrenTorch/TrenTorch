import numpy as np


def sample_lambda(alpha: float, rng: np.random.RandomState) -> float:
    """lam ~ Beta(alpha, alpha), one call to rng.beta."""
    # TODO
    pass


def mixup(x1, y1, x2, y2, lam: float):
    """Convex combination of two images and their one-hot labels."""
    # TODO
    pass
