import numpy as np


def mgf(values, probabilities, t):
    values = np.asarray(values, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    t = np.asarray(t, dtype=float)
    total = (probabilities * np.exp(t[..., None] * values)).sum(axis=-1)
    return total if total.ndim else float(total)


def pgf(probabilities, z):
    probabilities = np.asarray(probabilities, dtype=float)
    z = np.asarray(z, dtype=float)
    powers = z[..., None] ** np.arange(len(probabilities))
    total = (probabilities * powers).sum(axis=-1)
    return total if total.ndim else float(total)


def mgf_moments(mgf_fn, step=1e-3):
    h = step
    first = (mgf_fn(h) - mgf_fn(-h)) / (2.0 * h)
    second = (mgf_fn(h) - 2.0 * mgf_fn(0.0) + mgf_fn(-h)) / h**2
    return float(first), float(second)


def pgf_mean_variance(probabilities):
    p = np.asarray(probabilities, dtype=float)
    k = np.arange(len(p))
    first_derivative = float(np.sum(k * p))
    second_derivative = float(np.sum(k * (k - 1) * p))
    variance = second_derivative + first_derivative - first_derivative**2
    return first_derivative, float(variance)


def sum_distribution(p, q):
    return np.convolve(np.asarray(p, dtype=float), np.asarray(q, dtype=float))
