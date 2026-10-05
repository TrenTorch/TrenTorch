import numpy as np


def stratified_train_test_split(
    y: np.ndarray, test_fraction: float = 0.25, seed: int = 0
) -> tuple[np.ndarray, np.ndarray]:
    if not 0.0 <= test_fraction <= 1.0:
        raise ValueError("test_fraction must lie in [0, 1]")
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    train, test = [], []
    for label in np.unique(y):
        indices = np.flatnonzero(y == label)
        rng.shuffle(indices)
        n_test = int(round(test_fraction * len(indices)))
        test.extend(indices[:n_test])
        train.extend(indices[n_test:])
    return np.sort(np.array(train, dtype=int)), np.sort(np.array(test, dtype=int))
