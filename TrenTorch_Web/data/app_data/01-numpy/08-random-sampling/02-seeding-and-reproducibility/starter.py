import numpy as np


def reproducible_draw(seed: int, n: int) -> np.ndarray:
    """
    Create a Generator from `seed` and return a 1D array of `n`
    random floats drawn from it with rng.random(n).
    Calling this twice with the same arguments must return
    identical arrays.
    """
    pass


def draw_twice(seed: int, n: int) -> tuple:
    """
    Create ONE Generator from `seed`. Draw `n` floats from it,
    then draw `n` more floats from the same Generator.
    Return the tuple (first, second).
    The two arrays must be different from each other.
    """
    pass


def same_seed_same_output(seed: int, n: int) -> bool:
    """
    Create two separate Generators from the same `seed`, draw `n`
    floats from each, and return True if the two arrays are exactly
    equal, False otherwise.
    """
    pass


def skip_then_draw(rng: np.random.Generator, skip: int, n: int) -> np.ndarray:
    """
    Discard the next `skip` random floats from `rng`, then return
    the following `n` floats as a 1D array.

    Both the discard and the draw must be made on the `rng` that was
    passed in (not on a new generator), so the caller's `rng` is left
    advanced by skip + n draws.
    """
    pass
