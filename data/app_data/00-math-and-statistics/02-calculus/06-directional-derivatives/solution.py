import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

gradient = load_solution("00-math-and-statistics/02-calculus/02-partial-derivatives").gradient


def directional_derivative(f, x: np.ndarray, direction: np.ndarray, eps: float = 1e-5) -> float:
    unit_direction = direction / np.linalg.norm(direction)
    return (f(x + eps * unit_direction) - f(x - eps * unit_direction)) / (2 * eps)


def steepest_ascent_direction(f, x: np.ndarray) -> np.ndarray:
    grad = gradient(f, x)
    return grad / np.linalg.norm(grad)
