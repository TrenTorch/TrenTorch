import numpy as np


def expected_calibration_error(confidences, correct, n_bins: int = 10) -> float:
    """Weighted mean gap between accuracy and confidence over equal-width bins."""
    # TODO
    pass


def brier_score(probs, outcomes) -> float:
    """Mean squared error between predicted probabilities and 0/1 outcomes."""
    # TODO
    pass
