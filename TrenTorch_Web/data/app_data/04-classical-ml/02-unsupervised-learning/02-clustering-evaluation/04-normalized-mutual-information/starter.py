import numpy as np


def normalized_mutual_information(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    """
    MI / ((H(true) + H(pred)) / 2), in [0, 1]. Returns 1.0 when both
    labelings have a single cluster. Raises ValueError on length mismatch.
    """
    pass
