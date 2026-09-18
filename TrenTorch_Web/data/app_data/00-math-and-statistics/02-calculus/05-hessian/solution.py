import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

gradient = load_solution("00-math-and-statistics/02-calculus/02-partial-derivatives").gradient


def hessian(f, x: np.ndarray, eps: float = 1e-4) -> np.ndarray:
    n = len(x)
    result = np.zeros((n, n))
    for i in range(n):
        x_plus = x.copy()
        x_plus[i] += eps
        x_minus = x.copy()
        x_minus[i] -= eps
        result[:, i] = (gradient(f, x_plus) - gradient(f, x_minus)) / (2 * eps)
    return result


def classify_critical_point(hessian_matrix: np.ndarray) -> str:
    eigenvalues = np.linalg.eigvalsh(hessian_matrix)
    if np.all(eigenvalues > 1e-6):
        return "minimum"
    if np.all(eigenvalues < -1e-6):
        return "maximum"
    return "saddle"
