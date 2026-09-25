import numpy as np


def reproducible_draw(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.random(n)


def draw_twice(seed: int, n: int) -> tuple:
    rng = np.random.default_rng(seed)
    first = rng.random(n)
    second = rng.random(n)
    return first, second


def same_seed_same_output(seed: int, n: int) -> bool:
    rng_a = np.random.default_rng(seed)
    rng_b = np.random.default_rng(seed)
    return bool(np.array_equal(rng_a.random(n), rng_b.random(n)))


def skip_then_draw(rng: np.random.Generator, skip: int, n: int) -> np.ndarray:
    rng.random(skip)
    return rng.random(n)
