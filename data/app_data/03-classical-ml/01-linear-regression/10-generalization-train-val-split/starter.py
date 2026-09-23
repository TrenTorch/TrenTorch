import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402


def train_val_split(
    input: np.ndarray, target: np.ndarray, val_fraction: float = 0.2, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Shuffles `input`/`target` together (so a row's features and its
    target stay paired), then splits off `val_fraction` of the rows as
    a held-out validation set.

    Returns (input_train, target_train, input_val, target_val).
    """
    pass


def generalization_gap(train_loss: float, val_loss: float) -> float:
    """
    The generalization gap: how much worse the model performs on data
    it never trained on, compared to the data it did. A large positive
    gap is the numerical signature of overfitting.
    """
    pass
