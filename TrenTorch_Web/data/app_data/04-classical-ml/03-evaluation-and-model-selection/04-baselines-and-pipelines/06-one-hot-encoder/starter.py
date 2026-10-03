import numpy as np


def one_hot_fit(values) -> list:
    """
    Sorted list of the distinct values in values. This list fixes the
    column order for one_hot_transform.
    """
    pass


def one_hot_transform(values, categories) -> np.ndarray:
    """
    Float matrix of shape (len(values), len(categories)). Column j is 1
    where the value equals categories[j]. Raises ValueError for any
    value not in categories.
    """
    pass
