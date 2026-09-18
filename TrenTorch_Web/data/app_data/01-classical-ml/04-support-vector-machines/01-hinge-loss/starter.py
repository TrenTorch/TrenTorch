import numpy as np


def hinge_loss(scores: np.ndarray, target: np.ndarray, reduction: str = "mean") -> float | np.ndarray:
    """
    target: labels in {-1, +1} (NOT {0, 1}, the convention every
    binary classification question so far has used, SVMs conventionally
    use +-1 instead, see Theory for why).
    scores: raw, unbounded classifier outputs (like linear's own
    output, NOT passed through sigmoid).

        hinge_loss = max(0, 1 - target * scores)

    reduction: "mean" (default), "sum", or "none".
    """
    pass
