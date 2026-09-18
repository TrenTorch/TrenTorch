import numpy as np


def train_test_split(
    input: np.ndarray, labels: np.ndarray, test_size: float, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n_samples = input.shape[0]
    shuffled_idx = rng.permutation(n_samples)

    n_test = int(round(n_samples * test_size))
    test_idx = shuffled_idx[:n_test]
    train_idx = shuffled_idx[n_test:]

    return input[train_idx], input[test_idx], labels[train_idx], labels[test_idx]


def k_fold_split(
    n_samples: int, k: int, seed: int | None = None
) -> list[tuple[np.ndarray, np.ndarray]]:
    rng = np.random.default_rng(seed)
    shuffled_idx = rng.permutation(n_samples)
    folds = np.array_split(shuffled_idx, k)

    splits = []
    for i in range(k):
        val_idx = folds[i]
        train_idx = np.concatenate([folds[j] for j in range(k) if j != i])
        splits.append((train_idx, val_idx))
    return splits
