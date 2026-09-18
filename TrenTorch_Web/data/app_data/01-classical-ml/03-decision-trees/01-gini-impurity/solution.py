import numpy as np


def gini_impurity(labels: np.ndarray) -> float:
    if labels.size == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    probabilities = counts / labels.size
    return float(1.0 - np.sum(probabilities**2))
