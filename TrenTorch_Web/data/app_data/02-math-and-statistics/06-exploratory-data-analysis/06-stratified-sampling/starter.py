import numpy as np


def class_proportions(labels: np.ndarray) -> dict:
    """
    Returns {label: fraction_of_dataset_with_this_label}, one entry
    per distinct value in `labels`. Fractions sum to 1.0.
    """
    pass


def stratified_sample_indices(labels: np.ndarray, sample_size: int, seed: int | None = None) -> np.ndarray:
    """
    Draws a sample of roughly `sample_size` total indices (may be
    slightly smaller after rounding per class) such that each class is
    represented in roughly the SAME proportion it has in the full
    `labels` array, sampling WITHOUT replacement within each class.

    Returns an array of indices into `labels` (not the labels
    themselves).
    """
    pass
