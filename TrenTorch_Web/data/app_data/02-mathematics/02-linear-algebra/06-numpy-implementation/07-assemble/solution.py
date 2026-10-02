import numpy as np


def solve_and_verify(coefficients: np.ndarray, constants: np.ndarray) -> dict:
    is_solvable = abs(np.linalg.det(coefficients)) > 1e-10

    if not is_solvable:
        return {"is_solvable": False, "solution": None, "residual_norm": None}

    solution = np.linalg.solve(coefficients, constants)
    residual = coefficients @ solution - constants
    residual_norm = np.linalg.norm(residual)

    return {
        "is_solvable": True,
        "solution": solution,
        "residual_norm": residual_norm,
    }
