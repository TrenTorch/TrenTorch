import numpy as np


def create_rng(seed: int) -> np.random.Generator:
    """
    Create and return a new Generator initialized with `seed`,
    using np.random.default_rng(seed).

    Must NOT use the legacy global API (np.random.seed or
    np.random.rand and similar), and must not alter the state of
    the legacy global generator.
    """
    pass


def make_independent_rngs(seed_a: int, seed_b: int) -> tuple:
    """
    Return a tuple (rng_a, rng_b) of two separate Generator objects,
    created from seed_a and seed_b respectively.

    Drawing values from one must have no effect on the values the
    other produces.
    """
    pass


def draw(rng: np.random.Generator, n: int) -> np.ndarray:
    """
    Return a 1D array of `n` random floats drawn from `rng`,
    using rng.random(n). This advances the state of `rng`.
    """
    pass
