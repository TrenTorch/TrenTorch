import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

soft_threshold = load_solution(
    "01-classical-ml/03-regularized-linear-models/03-lasso-regression"
).soft_threshold


def elastic_net_coordinate_descent(
    input: np.ndarray,
    target: np.ndarray,
    alpha: float = 1.0,
    l1_ratio: float = 0.5,
    epochs: int = 200,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Elastic Net combines Ridge's L2 penalty and Lasso's L1 penalty in
    one loss, `l1_ratio` (in [0, 1]) controls the mix: l1_ratio=1.0 is
    pure Lasso, l1_ratio=0.0 is pure Ridge.

    Reuses Lasso's own coordinate descent structure and its
    soft_threshold building block (already provided above), with one
    change: the single-coordinate update also divides by an extra
    L2-penalty term, exactly like Ridge's own extra term.

    Returns (weight, bias) in the same shapes the other regression
    questions in this curriculum use.
    """
    pass
