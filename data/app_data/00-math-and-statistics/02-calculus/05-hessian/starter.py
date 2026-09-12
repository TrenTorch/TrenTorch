import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

gradient = load_solution("00-math-and-statistics/02-calculus/02-partial-derivatives").gradient


def hessian(f, x: np.ndarray, eps: float = 1e-4) -> np.ndarray:
    """
    f: R^n -> R (a scalar-valued function, like a loss). Returns the
    (n, n) Hessian matrix of second partial derivatives:

        H[i, j] = d^2f / (dx_i dx_j)

    Compute it as the Jacobian of the gradient: nudge coordinate i up
    and down by eps, evaluate the FULL gradient (already provided
    above) at each nudged point, and central-difference those two
    gradient vectors to fill column i of H. This mirrors 04-jacobian's
    structure exactly, but applied to `gradient` instead of `f` itself.

    A larger default eps than 01-derivatives-first-principles' 1e-5 is
    used here on purpose: differentiating a function that is ITSELF
    already a finite-difference approximation amplifies floating-point
    error, a larger step keeps that error manageable.
    """
    pass


def classify_critical_point(hessian_matrix: np.ndarray) -> str:
    """
    At a point where the gradient is zero, the Hessian's eigenvalues
    (08-positive-definite-matrices) tell you what kind of critical
    point you're at:

        every eigenvalue > 0  -> "minimum"
        every eigenvalue < 0  -> "maximum"
        mixed signs           -> "saddle"

    Use a small tolerance around zero (an eigenvalue that is
    essentially zero, within floating-point noise, is neither cleanly
    positive nor negative) rather than a bare `> 0`.
    """
    pass
