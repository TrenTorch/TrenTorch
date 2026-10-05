import numpy as np


def average_precision(y_true: np.ndarray, scores: np.ndarray) -> float:
    """
    Area under the precision-recall step curve for binary labels, with
    higher scores meaning more likely positive. Ties are evaluated as one
    threshold. Raises ValueError on length mismatch or when there are no
    positives.
    """
    pass
