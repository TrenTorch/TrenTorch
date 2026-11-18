import numpy as np


def dropout_expectation(x, p, n_samples, rng):
    """
    x: activations (NumPy array)
    p: drop probability (0 <= p < 1)
    n_samples: number of independent dropout masks to average over
    rng: a NumPy Generator used to draw the masks

    Returns:
        The mean of the inverted-dropout outputs over `n_samples` masks.
        As n_samples grows, this approaches x.
    """
    # TODO: Draw n_samples keep masks, apply inverted dropout to each, and average.
    pass
