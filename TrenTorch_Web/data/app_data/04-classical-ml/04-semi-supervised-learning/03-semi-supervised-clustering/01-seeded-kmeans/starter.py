import numpy as np


def seeded_kmeans(X: np.ndarray, seeds: np.ndarray, k: int, iters: int = 100):
    """
    Seeded k-means. seeds[i] is a class in 0..k-1 for seeded points and -1
    otherwise. Returns (labels, centroids). Raise ValueError if a class has no
    seed, a seed is out of range, or shapes are inconsistent.
    """
    pass
