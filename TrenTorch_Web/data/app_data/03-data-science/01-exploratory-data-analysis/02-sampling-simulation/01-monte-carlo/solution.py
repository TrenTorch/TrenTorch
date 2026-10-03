import math

import numpy as np


def monte_carlo_mean(f, sampler, n: int, rng: np.random.Generator) -> tuple:
    values = np.asarray(f(sampler(rng, n)), dtype=float)
    return float(values.mean()), float(values.std(ddof=1) / math.sqrt(n))


def estimate_pi(n: int, rng: np.random.Generator) -> float:
    x = rng.random(n)
    y = rng.random(n)
    inside = int(np.sum(x**2 + y**2 <= 1.0))
    return float(4.0 * inside / n)


def monte_carlo_integral(f, a: float, b: float, n: int, rng: np.random.Generator) -> float:
    u = rng.uniform(a, b, size=n)
    return float((b - a) * np.mean(f(u)))


def samples_for_precision(std: float, target_se: float) -> int:
    if target_se <= 0:
        raise ValueError("target_se must be positive")
    return int(math.ceil((std / target_se) ** 2))
