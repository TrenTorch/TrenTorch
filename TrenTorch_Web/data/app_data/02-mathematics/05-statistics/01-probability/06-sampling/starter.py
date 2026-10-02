import numpy as np


def sample_normal(mean: float, std: float, size: int, seed: int | None = None) -> np.ndarray:
    """
    Draw `size` independent samples from a Normal(mean, std) distribution.

    Use np.random.default_rng(seed), NumPy's modern, seedable random
    generator (not the legacy np.random.seed/np.random.normal global
    state, which is stateful in a way that silently interacts badly
    across unrelated code that also touches the global RNG).
    """
    pass


def empirical_histogram(samples: np.ndarray, bins: int = 10):
    """
    Bucket `samples` into `bins` equal-width bins and count how many
    samples fall in each one. Returns (counts, bin_edges), mirroring
    np.histogram's own return signature (bin_edges has length
    len(counts) + 1: one boundary more than there are bins).
    """
    pass
