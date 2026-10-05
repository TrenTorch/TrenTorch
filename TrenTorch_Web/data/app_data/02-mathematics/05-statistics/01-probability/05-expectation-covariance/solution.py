import numpy as np


def expectation(values, probabilities):
    values = np.asarray(values, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    return float(np.sum(values * probabilities))


def variance(values, probabilities):
    values = np.asarray(values, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    mean = expectation(values, probabilities)
    return float(np.sum(probabilities * (values - mean) ** 2))


def pmf_covariance(x_values, y_values, joint_probabilities):
    x_values = np.asarray(x_values, dtype=float)
    y_values = np.asarray(y_values, dtype=float)
    joint_probabilities = np.asarray(joint_probabilities, dtype=float)

    marginal_x = joint_probabilities.sum(axis=1)
    marginal_y = joint_probabilities.sum(axis=0)
    mean_x = expectation(x_values, marginal_x)
    mean_y = expectation(y_values, marginal_y)

    total = 0.0
    for i, x in enumerate(x_values):
        for j, y in enumerate(y_values):
            total += joint_probabilities[i, j] * (x - mean_x) * (y - mean_y)
    return float(total)


def sample_mean(x: np.ndarray) -> float:
    return float(np.mean(x))


def sample_variance(x: np.ndarray, ddof: int = 0) -> float:
    return float(np.var(x, ddof=ddof))


def covariance(x: np.ndarray, y: np.ndarray, ddof: int = 0) -> float:
    n = len(x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    return float(np.sum((x - mean_x) * (y - mean_y)) / (n - ddof))


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    return float(covariance(x, y) / (np.std(x) * np.std(y)))
