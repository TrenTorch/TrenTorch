import numpy as np


def sample_normal(
    rng: np.random.Generator, mean: float, std: float, shape: tuple
) -> np.ndarray:
    """
    Return an array of the given `shape` with elements drawn from a
    normal distribution with the given `mean` and `std`, using
    rng.normal(mean, std, shape).
    """
    pass


def empirical_mean_std(samples: np.ndarray) -> tuple:
    """
    Return (mean, std) of ALL elements in `samples`, as two Python
    floats, regardless of the array's shape.
    """
    pass


def he_init(rng: np.random.Generator, fan_in: int, fan_out: int) -> np.ndarray:
    """
    Return a weight matrix of shape (fan_in, fan_out) whose elements
    are drawn from a normal distribution with mean 0 and standard
    deviation sqrt(2 / fan_in), using
    rng.normal(0.0, np.sqrt(2.0 / fan_in), (fan_in, fan_out)).
    """
    pass
