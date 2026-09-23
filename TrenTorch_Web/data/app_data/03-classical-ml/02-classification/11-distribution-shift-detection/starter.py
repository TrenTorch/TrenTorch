import numpy as np

_EPS = 1e-6


def bin_proportions(values: np.ndarray, bin_edges: np.ndarray) -> np.ndarray:
    """
    Buckets `values` into the bins defined by `bin_edges` (same idea as
    01-outlier-detection's histogram, Math & Statistics) and returns
    the FRACTION of values landing in each bin (not raw counts).
    """
    pass


def population_stability_index(
    train_values: np.ndarray, live_values: np.ndarray, num_bins: int = 10
) -> float:
    """
    The Population Stability Index (PSI): a standard production-ML
    metric for whether a feature's live distribution has drifted away
    from its training-time distribution.

    Bin edges are chosen from TRAINING data's quantiles (so each bin
    holds roughly 1/num_bins of the training data by construction),
    with the outermost edges widened to -inf/+inf so no live value
    ever falls outside every bin. Then:

        PSI = sum_bins( (live_pct - train_pct) * log(live_pct / train_pct) )

    Clip both proportion arrays away from exactly 0 before the log,
    for the same reason 01-entropy (Math & Statistics) clips.
    """
    pass


def detect_distribution_shift(
    train_values: np.ndarray, live_values: np.ndarray, num_bins: int = 10, threshold: float = 0.2
) -> bool:
    """
    Flags a meaningful distribution shift using the conventional PSI
    threshold: PSI > 0.2 is generally considered a significant shift
    in production ML monitoring practice.
    """
    pass
