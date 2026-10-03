import numpy as np


def _entropy(labels: np.ndarray) -> float:
    if labels.size == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    p = counts / labels.size
    return float(-np.sum(p * np.log2(p)))


def gain_ratio(feature: np.ndarray, labels: np.ndarray) -> float:
    n = labels.size
    if n == 0:
        return 0.0
    values, counts = np.unique(feature, return_counts=True)
    weights = counts / n
    conditional = sum(w * _entropy(labels[feature == v]) for v, w in zip(values, weights))
    gain = _entropy(labels) - conditional
    intrinsic = float(-np.sum(weights * np.log2(weights)))
    if intrinsic == 0.0:
        return 0.0
    return float(gain / intrinsic)
