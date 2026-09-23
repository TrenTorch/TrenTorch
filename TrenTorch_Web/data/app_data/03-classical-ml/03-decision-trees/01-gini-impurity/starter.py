import numpy as np


def gini_impurity(labels: np.ndarray) -> float:
    """
    labels: 1-D array of class labels (any integers, not necessarily
    0..k-1 or contiguous), one per sample in a single tree node.

    Returns:
        the Gini impurity of this set of labels, a float in [0, 1).
    """
    # TODO: Implement the Gini impurity formula from Theory.
    # An empty labels array has no impurity by convention -- return 0.0.
    pass
