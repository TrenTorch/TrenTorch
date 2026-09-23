import numpy as np


def normalize_image(matrix: np.ndarray) -> tuple[float, float, np.ndarray]:
    """
    Z-score normalize an image by its own mean and population std.

    matrix: shape (H, W).

    Return (mu, sigma, normalized) where mu and sigma are the mean and
    population standard deviation (divide by n, not n - 1) of every pixel,
    and normalized = (matrix - mu) / sigma.

    A constant image (sigma == 0.0) has no spread to divide by: return an
    all-zero normalized array of the same shape instead of dividing.
    """
    # TODO: matrix.std() with the default ddof already gives the population std.
    pass
