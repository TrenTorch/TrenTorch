import numpy as np


def solve_system(coefficients: np.ndarray, constants: np.ndarray) -> np.ndarray:
    return np.linalg.solve(coefficients, constants)


def solve_via_inverse(coefficients: np.ndarray, constants: np.ndarray) -> np.ndarray:
    return np.linalg.inv(coefficients) @ constants


def solutions_agree(coefficients: np.ndarray, constants: np.ndarray) -> bool:
    return bool(
        np.allclose(
            solve_system(coefficients, constants),
            solve_via_inverse(coefficients, constants),
        )
    )
