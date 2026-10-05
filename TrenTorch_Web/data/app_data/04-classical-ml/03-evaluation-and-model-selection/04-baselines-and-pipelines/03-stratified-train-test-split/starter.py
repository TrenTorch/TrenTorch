import numpy as np


def stratified_train_test_split(
    y: np.ndarray, test_fraction: float = 0.25, seed: int = 0
) -> tuple[np.ndarray, np.ndarray]:
    """
    Split indices so each class keeps its proportion on both sides.
    For each class, round(test_fraction * class_count) members go to the
    test set, chosen with a generator seeded by seed. Returns
    (train_indices, test_indices), both sorted. Raises ValueError when
    test_fraction is outside [0, 1].
    """
    pass
