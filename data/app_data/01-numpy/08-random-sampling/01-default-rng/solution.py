import numpy as np


def create_rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def make_independent_rngs(seed_a: int, seed_b: int) -> tuple:
    return np.random.default_rng(seed_a), np.random.default_rng(seed_b)


def draw(rng: np.random.Generator, n: int) -> np.ndarray:
    return rng.random(n)
