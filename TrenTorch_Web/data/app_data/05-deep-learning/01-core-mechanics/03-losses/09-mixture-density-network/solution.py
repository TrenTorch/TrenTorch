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
    y = np.atleast_1d(y)
    pi = np.atleast_2d(pi)
    mu = np.atleast_2d(mu)
    sigma = np.atleast_2d(sigma)

    n_samples = y.shape[0]

    if pi.shape[0] != n_samples or mu.shape[0] != n_samples or sigma.shape[0] != n_samples:
        raise ValueError("First dimension must match across y, pi, mu, sigma")

    if pi.shape[1] != mu.shape[1] or pi.shape[1] != sigma.shape[1]:
        raise ValueError("Second dimension must match across pi, mu, sigma (number of components)")

    if np.any(sigma <= 0):
        raise ValueError("sigma must be positive")

    y_expanded = y[:, np.newaxis]

    numerator = np.exp(-0.5 * ((y_expanded - mu) / sigma) ** 2)
    denominator = sigma * np.sqrt(2.0 * np.pi)

    gaussian_pdf = numerator / denominator

    mixture_pdf = np.sum(pi * gaussian_pdf, axis=1)

    mixture_pdf = np.clip(mixture_pdf, 1e-10, None)

    loss = -np.mean(np.log(mixture_pdf))

    return loss
