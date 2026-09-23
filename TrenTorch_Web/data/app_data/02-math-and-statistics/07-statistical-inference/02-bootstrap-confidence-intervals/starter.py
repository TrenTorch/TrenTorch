import numpy as np


def bootstrap_resample(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Draws a resample the SAME size as x, WITH replacement (some
    original values may appear multiple times, others not at all).
    This is the defining move of the bootstrap: treat the observed
    sample itself as a stand-in for the whole population, and resample
    from it as if it were that population.
    """
    pass


def bootstrap_confidence_interval(
    x: np.ndarray,
    statistic_fn,
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
    seed: int | None = None,
) -> tuple[float, float]:
    """
    `01-confidence-interval`'s t-based interval only has a known
    closed-form solution for the MEAN. The bootstrap generalizes to
    ANY statistic (median, std, a custom function, anything): resample
    x with replacement `n_bootstrap` times, compute `statistic_fn` on
    each resample, and use the PERCENTILES of that whole distribution
    of resampled statistics as the interval bounds.

    Returns (lower, upper): the (1-confidence)/2 and (1+confidence)/2
    percentiles of the bootstrap distribution.
    """
    pass
