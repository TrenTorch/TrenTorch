import numpy as np


def rand_index(labels_a: np.ndarray, labels_b: np.ndarray) -> float:
    """
    labels_a, labels_b: 1-D cluster assignments of the same samples.

    Returns:
        fraction of sample pairs on which the two partitions agree
        (1.0 if there are fewer than two samples).
    """
    # TODO: Compare "same cluster?" for every pair under both partitions.
    pass
