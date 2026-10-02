import numpy as np


def skewness(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    std = x.std()
    if std == 0.0:
        return 0.0
    return float(np.mean(((x - x.mean()) / std) ** 3))


def log1p_transform(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if np.any(x < 0):
        raise ValueError("log1p_transform needs non-negative values")
    return np.log1p(x)


def inverse_log1p(z: np.ndarray) -> np.ndarray:
    return np.expm1(np.asarray(z, dtype=float))


def box_cox(x: np.ndarray, lam: float) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if np.any(x <= 0):
        raise ValueError("box_cox needs strictly positive values")
    if lam == 0:
        return np.log(x)
    return (x**lam - 1.0) / lam


def best_box_cox_lambda(x: np.ndarray, candidates: list) -> float:
    return min(candidates, key=lambda lam: abs(skewness(box_cox(x, lam))))
