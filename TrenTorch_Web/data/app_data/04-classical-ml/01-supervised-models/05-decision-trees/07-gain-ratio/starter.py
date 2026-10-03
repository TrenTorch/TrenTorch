import numpy as np


def gain_ratio(feature: np.ndarray, labels: np.ndarray) -> float:
    """
    feature: 1-D array, one categorical value per sample.
    labels: 1-D array of class labels, same length as feature.

    Returns:
        information gain of splitting on `feature`, divided by the
        split's intrinsic value (base-2 logs). 0.0 if the input is
        empty or the feature has only one distinct value.
    """
    # TODO: Implement gain ratio from Theory.
    pass
