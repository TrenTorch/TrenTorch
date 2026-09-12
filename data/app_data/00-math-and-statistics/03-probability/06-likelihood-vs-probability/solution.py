import numpy as np


def normal_pdf(x: np.ndarray, mean: float, std: float) -> np.ndarray:
    coefficient = 1.0 / (std * np.sqrt(2.0 * np.pi))
    exponent = -0.5 * ((x - mean) / std) ** 2
    return coefficient * np.exp(exponent)


def joint_density(x_values: np.ndarray, mean: float, std: float) -> float:
    return float(np.prod(normal_pdf(x_values, mean, std)))


def likelihood_curve(x_values: np.ndarray, candidate_means: np.ndarray, std: float) -> np.ndarray:
    return np.array([joint_density(x_values, mean, std) for mean in candidate_means])
