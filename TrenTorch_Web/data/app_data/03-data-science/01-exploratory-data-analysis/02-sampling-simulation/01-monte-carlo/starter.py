import numpy as np


def monte_carlo_mean(f, sampler, n: int, rng: np.random.Generator) -> tuple:
    """
    f: vectorized function, takes an array of draws and returns an array
    sampler: sampler(rng, n) returns a 1D array of n independent draws
    n: number of draws (n >= 2)

    Calls sampler exactly once. Returns (estimate, standard_error) as
    floats: the mean of f(samples) and its sample standard deviation
    (ddof=1) divided by sqrt(n).
    """
    # TODO: Average f over the draws and compute the standard error.
    pass


def estimate_pi(n: int, rng: np.random.Generator) -> float:
    """
    Draws x = rng.random(n) and then y = rng.random(n), counts the points
    with x**2 + y**2 <= 1 and returns 4 * count / n as a float.
    """
    # TODO: Use the fraction of points inside the quarter circle.
    pass


def monte_carlo_integral(f, a: float, b: float, n: int, rng: np.random.Generator) -> float:
    """
    Draws u = rng.uniform(a, b, size=n) once and returns
    (b - a) * mean(f(u)) as a float. f is vectorized.
    """
    # TODO: Use the interval length times the average of f.
    pass


def samples_for_precision(std: float, target_se: float) -> int:
    """
    Returns the smallest integer n with std / sqrt(n) <= target_se.

    Raises:
        ValueError: if target_se <= 0.
    """
    # TODO: Solve the standard error formula for n.
    pass
