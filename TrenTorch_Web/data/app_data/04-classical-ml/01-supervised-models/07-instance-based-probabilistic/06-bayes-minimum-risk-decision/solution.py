import numpy as np


def minimum_risk_class(posteriors: np.ndarray, cost_matrix: np.ndarray) -> int:
    risks = np.asarray(posteriors, dtype=float) @ np.asarray(cost_matrix, dtype=float)
    return int(np.argmin(risks))
