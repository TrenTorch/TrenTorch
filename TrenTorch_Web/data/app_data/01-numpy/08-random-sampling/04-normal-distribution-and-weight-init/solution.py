import numpy as np


def sample_normal(
    rng: np.random.Generator, mean: float, std: float, shape: tuple
) -> np.ndarray:
    return rng.normal(mean, std, shape)


def empirical_mean_std(samples: np.ndarray) -> tuple:
    return float(samples.mean()), float(samples.std())


def he_init(rng: np.random.Generator, fan_in: int, fan_out: int) -> np.ndarray:
    scale = np.sqrt(2.0 / fan_in)
    return rng.normal(0.0, scale, (fan_in, fan_out))
