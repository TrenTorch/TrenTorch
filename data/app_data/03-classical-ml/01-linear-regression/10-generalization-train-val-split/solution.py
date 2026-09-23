import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402


def train_val_split(
    input: np.ndarray, target: np.ndarray, val_fraction: float = 0.2, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = len(input)
    shuffled_indices = rng.permutation(n)
    val_size = round(n * val_fraction)
    val_indices = shuffled_indices[:val_size]
    train_indices = shuffled_indices[val_size:]
    return input[train_indices], target[train_indices], input[val_indices], target[val_indices]


def generalization_gap(train_loss: float, val_loss: float) -> float:
    return val_loss - train_loss
