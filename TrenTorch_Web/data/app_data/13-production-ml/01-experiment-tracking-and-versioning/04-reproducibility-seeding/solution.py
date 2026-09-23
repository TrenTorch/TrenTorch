import random

import numpy as np


def seeded_numpy_sequence(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.random(n)


def seeded_python_random_sequence(seed: int, n: int) -> list:
    rng = random.Random(seed)
    return [rng.random() for _ in range(n)]


def capture_reproducibility_config(numpy_seed: int, python_seed: int) -> dict:
    return {"numpy_seed": numpy_seed, "python_random_seed": python_seed}


def verify_reproducible(fn, seed: int, num_trials: int = 3) -> bool:
    results = [fn(seed) for _ in range(num_trials)]
    first = results[0]
    return all(np.array_equal(first, r) for r in results[1:])
