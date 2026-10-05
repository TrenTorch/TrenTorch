import numpy as np


def mdn_loss(y, pi, mu, sigma):
    """Compute Mixture Density Network loss.

    Args:
        y: Target values (shape N,).
        pi: Mixture weights (shape N, K), sum to 1 per sample.
        mu: Gaussian means (shape N, K).
        sigma: Gaussian standard deviations (shape N, K), all > 0.

    Returns:
        Scalar loss value.

    Raises:
        ValueError: If shapes don't match or sigma <= 0.
    """
    pass
