import numpy as np


def uniform_array(
    rng: np.random.Generator, low: float, high: float, shape: tuple
) -> np.ndarray:
    """
    Return an array of the given `shape` whose elements are drawn
    uniformly from [low, high), using `rng`.
    """
    pass


def random_integers(
    rng: np.random.Generator, low: int, high: int, shape: tuple
) -> np.ndarray:
    """
    Return an integer array of the given `shape` whose elements are
    drawn from [low, high) — `high` is EXCLUDED — using `rng`.
    """
    pass


def roll_dice(rng: np.random.Generator, n_dice: int, sides: int) -> np.ndarray:
    """
    Simulate rolling `n_dice` dice, each with faces numbered
    1 through `sides` INCLUSIVE. Return a 1D integer array of length
    `n_dice`, using `rng`.
    """
    pass
