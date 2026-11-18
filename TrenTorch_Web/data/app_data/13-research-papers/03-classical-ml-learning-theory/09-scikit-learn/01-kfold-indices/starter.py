import numpy as np


def kfold_indices(n, k):
    """
    n: number of samples
    k: number of folds

    Returns:
        A list of k (train_indices, test_indices) pairs. The test folds partition
        range(n), and their sizes differ by at most one.
    """
    # TODO: Split the indices into k contiguous folds and build each train/test pair (see Theory).
    pass
