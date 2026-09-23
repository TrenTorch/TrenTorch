import numpy as np


def cast_to_dtype(x: np.ndarray, dtype: str) -> np.ndarray:
    return x.astype(dtype)


def detect_underflow(original: np.ndarray, casted: np.ndarray) -> np.ndarray:
    return (original != 0.0) & (casted == 0.0)


def detect_overflow(casted: np.ndarray) -> np.ndarray:
    return np.isinf(casted)
