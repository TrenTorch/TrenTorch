import numpy as np


def soft_threshold(x: np.ndarray, threshold: float) -> np.ndarray:
    """
    The soft-thresholding operator, the core building block of Lasso's
    solver: shrinks x toward zero by `threshold`, snapping anything
    within `threshold` of zero to EXACTLY zero.

        soft_threshold(x, t) = sign(x) * max(|x| - t, 0)
    """
    pass


def lasso_regression_coordinate_descent(
    input: np.ndarray, target: np.ndarray, alpha: float = 1.0, epochs: int = 200
) -> tuple[np.ndarray, np.ndarray]:
    """
    Ridge Regression (L2) has a clean closed form; Lasso's L1 penalty
    does NOT (it's not differentiable at exactly 0), so this uses
    coordinate descent instead: repeatedly update ONE weight at a
    time, holding every other weight fixed, using soft_threshold to
    solve that single-coordinate subproblem exactly, cycling through
    all coordinates for several epochs.

    Center `input` and `target` first (subtract their means) so the
    bias can be recovered afterward without needing to include it in
    the penalized coordinate descent loop at all.

    Returns (weight, bias) in the same (1, in_features)/(1,) shapes
    the other regression questions in this curriculum use.
    """
    pass
