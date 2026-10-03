import numpy as np


def mixture_weights(sizes, temperature: float) -> np.ndarray:
    """Weights proportional to sizes ** (1 / temperature), summing to 1."""
    # TODO
    pass


def epochs_per_source(sizes, weights, total_tokens: float) -> np.ndarray:
    """How many passes over each source: weights * total_tokens / sizes."""
    # TODO
    pass
