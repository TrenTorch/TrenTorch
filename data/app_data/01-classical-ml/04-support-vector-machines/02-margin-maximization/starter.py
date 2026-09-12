import numpy as np


def functional_margin(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    y * (X @ weight + bias): positive when a point is correctly
    classified, its MAGNITUDE growing with how far the raw score sits
    past the decision boundary. Note: NOT scale-invariant, doubling
    weight and bias doubles this number without the decision boundary
    itself moving at all.
    """
    pass


def geometric_margin(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    The functional margin, rescaled by ||weight|| into an actual
    geometric DISTANCE from the decision boundary, in the same units
    as the input space itself. Unlike functional_margin, this IS
    scale-invariant: scaling weight and bias by any positive constant
    leaves this unchanged (see Theory for why).
    """
    pass


def dataset_margin(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray) -> float:
    """
    The SMALLEST geometric margin across the whole dataset, the
    distance from the decision boundary to its single closest correctly-
    classified point. This is exactly the quantity an SVM tries to
    maximize (see Theory), and the points that achieve it are the
    "support vectors" the model family is named for.
    """
    pass
