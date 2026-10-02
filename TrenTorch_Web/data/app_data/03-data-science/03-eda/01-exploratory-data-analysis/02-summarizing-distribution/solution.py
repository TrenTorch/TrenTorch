import numpy as np


def skewness(x: np.ndarray) -> float:
    mean = np.mean(x)
    std = np.std(x)
    return float(np.mean(((x - mean) / std) ** 3))


def summarize_distribution(x: np.ndarray) -> dict:
    return {
        "mean": float(np.mean(x)),
        "median": float(np.median(x)),
        "std": float(np.std(x)),
        "skew": skewness(x),
    }
