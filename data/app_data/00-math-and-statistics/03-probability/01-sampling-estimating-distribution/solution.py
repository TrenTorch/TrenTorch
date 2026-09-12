import numpy as np


def sample_normal(mean: float, std: float, size: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(loc=mean, scale=std, size=size)


def empirical_histogram(samples: np.ndarray, bins: int = 10):
    counts, edges = np.histogram(samples, bins=bins)
    return counts, edges
