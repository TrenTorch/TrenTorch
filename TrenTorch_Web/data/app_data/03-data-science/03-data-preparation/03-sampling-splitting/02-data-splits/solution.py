import numpy as np


def _sizes(n: int, val_fraction: float, test_fraction: float) -> tuple:
    n_test = int(round(test_fraction * n))
    n_val = int(round(val_fraction * n))
    return n - n_val - n_test, n_val, n_test


def train_val_test_split(n: int, val_fraction: float, test_fraction: float, rng: np.random.Generator) -> tuple:
    n_train, n_val, _ = _sizes(n, val_fraction, test_fraction)
    order = rng.permutation(n)
    return order[:n_train], order[n_train : n_train + n_val], order[n_train + n_val :]


def time_ordered_split(n: int, val_fraction: float, test_fraction: float) -> tuple:
    n_train, n_val, _ = _sizes(n, val_fraction, test_fraction)
    order = np.arange(n)
    return order[:n_train], order[n_train : n_train + n_val], order[n_train + n_val :]


def k_fold_indices(n: int, k: int, rng: np.random.Generator) -> list:
    blocks = np.array_split(rng.permutation(n), k)
    folds = []
    for i, block in enumerate(blocks):
        train = np.concatenate([b for j, b in enumerate(blocks) if j != i])
        folds.append((train, block))
    return folds


def expanding_window_splits(n: int, n_splits: int, min_train: int) -> list:
    splits = []
    for block in np.array_split(np.arange(min_train, n), n_splits):
        splits.append((np.arange(block[0]), block))
    return splits
