import numpy as np


def gaussian_kde(x: np.ndarray, grid: np.ndarray, bandwidth: float) -> np.ndarray:
    """
    x: 1D data array
    grid: 1D array of points at which to evaluate the density
    bandwidth: standard deviation of each Gaussian bump (> 0)

    Returns:
        An array the shape of grid where entry j is the average over the
        data of a Gaussian bump (standard deviation `bandwidth`) centred
        on each data point, evaluated at grid[j].

    Raises:
        ValueError: if bandwidth <= 0.
    """
    # TODO: Average one Gaussian bump per data point.
    pass


def silverman_bandwidth(x: np.ndarray) -> float:
    """
    Returns 0.9 * min(std, IQR / 1.34) * n ** (-1/5), with std the sample
    standard deviation (ddof=1) and IQR from np.percentile. If the
    smaller spread is zero use the other one, and 1.0 if both are zero.
    """
    # TODO: Implement Silverman's rule of thumb.
    pass


def integrate_density(density: np.ndarray, grid: np.ndarray) -> float:
    """
    Returns the trapezoid-rule area under `density` over the strictly
    increasing `grid`, as a float. Do not call np.trapz or np.trapezoid.
    """
    # TODO: Sum gap times average height over neighbouring grid points.
    pass
