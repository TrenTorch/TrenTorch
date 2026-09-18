import numpy as np


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sum(a * b))


def l1_norm(x: np.ndarray) -> float:
    return float(np.sum(np.abs(x)))


def l2_norm(x: np.ndarray) -> float:
    return float(np.sqrt(np.sum(x**2)))


def linf_norm(x: np.ndarray) -> float:
    return float(np.max(np.abs(x)))
