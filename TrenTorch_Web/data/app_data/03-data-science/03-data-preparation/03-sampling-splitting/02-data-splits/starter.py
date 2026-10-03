import numpy as np


def train_val_test_split(n: int, val_fraction: float, test_fraction: float, rng: np.random.Generator) -> tuple:
    """
    Shuffles with one rng.permutation(n). The test set has
    int(round(test_fraction * n)) indices, the validation set has
    int(round(val_fraction * n)) and training gets the rest. In the
    permutation the order is train, then validation, then test.
    Returns (train, val, test) as int index arrays.
    """
    # TODO: Permute the row numbers once and slice the permutation.
    pass


def time_ordered_split(n: int, val_fraction: float, test_fraction: float) -> tuple:
    """
    Same sizes as train_val_test_split but with no shuffling: the
    earliest rows train, the next block validates and the latest rows
    test, each in increasing order. Returns (train, val, test).
    """
    # TODO: Slice np.arange(n) instead of a permutation.
    pass


def k_fold_indices(n: int, k: int, rng: np.random.Generator) -> list:
    """
    Shuffles with one rng.permutation(n) and cuts it into k blocks with
    np.array_split. Returns a list of k pairs (train_indices,
    val_indices): val_indices is block i and train_indices is every other
    block concatenated in block order.
    """
    # TODO: Let each block take a turn as the validation set.
    pass


def expanding_window_splits(n: int, n_splits: int, min_train: int) -> list:
    """
    The rows after the first `min_train` are cut into n_splits contiguous
    blocks with np.array_split. Split i validates on block i and trains on
    every row before that block, in increasing order. Returns a list of
    n_splits pairs (train_indices, val_indices).
    """
    # TODO: Train on everything before each validation block.
    pass
