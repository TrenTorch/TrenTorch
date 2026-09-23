import numpy as np


def build_histogram(values: np.ndarray, n_bins: int) -> np.ndarray:
    """
    Returns n_bins + 1 evenly-spaced bin edges covering
    [values.min(), values.max()], the same shape np.linspace produces.
    """
    # TODO: one line, np.linspace over the min/max of values.
    pass


def find_best_split_histogram(
    input: np.ndarray, labels: np.ndarray, n_bins: int
) -> tuple[int, float, float] | None:
    """
    Like 03-best-split-minimal-tree's find_best_split, except candidate
    thresholds come from a fixed number of histogram bin boundaries per
    feature (build_histogram), not every unique value in the data.
    """
    # TODO: For each feature, build_histogram() it into n_bins bins,
    # then try only the INTERIOR bin edges (skip the first and last,
    # they'd put every sample on one side) as candidate thresholds,
    # scored with information_gain() same as find_best_split.
    pass
