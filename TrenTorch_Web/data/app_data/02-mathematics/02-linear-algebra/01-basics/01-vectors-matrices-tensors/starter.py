import numpy as np


def shape_of(x: np.ndarray) -> tuple:
    """
    A scalar is a 0-dimensional tensor, a vector is 1-dimensional, a
    matrix is 2-dimensional, and anything beyond that (a batch of
    images, a batch of sequences of embeddings, ...) is just called a
    tensor. Mirrors x.shape (equivalently x.size() in torch).

    Returns the shape as a tuple, e.g. (3,) for a length-3 vector,
    (2, 3) for a 2x3 matrix.
    """
    pass


def ndim_of(x: np.ndarray) -> int:
    """
    Mirrors x.ndim (equivalently x.dim() in torch): how many axes x has,
    i.e. len(shape_of(x)).
    """
    pass


def elementwise_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    a and b must have the same shape (or be broadcastable, see the
    Broadcasting track later). Adds them position by position.
    """
    pass


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Same shape rule as elementwise_add. This is NOT matrix
    multiplication (that's a separate, much less "obvious" operation
    covered later): elementwise multiply is just a[i] * b[i] at every
    position, so the inputs and the output all share one shape.
    """
    pass
