import numpy as np


def scalar_gradient_chain(depth: int, layer_scale: float) -> float:
    """
    The simplest possible model of backpropagating a gradient through a
    chain of `depth` layers, each of which scales the gradient passing
    through it by the SAME fixed factor `layer_scale` (a crude stand-in
    for "each layer's weight matrix has this scale"). Returns the final
    gradient magnitude after passing through all `depth` layers.
    """
    pass


def matrix_gradient_norms(
    depth: int, dim: int, weight_std: float, rng: np.random.RandomState
) -> list[float]:
    """
    A more realistic version: starts with a gradient vector of all 1s
    (length `dim`), and at each of `depth` layers, multiplies it by a
    FRESH random (dim, dim) weight matrix (entries drawn from
    N(0, weight_std^2)), exactly the repeated matrix multiplication real
    backpropagation performs layer by layer. Returns a list of the
    gradient vector's NORM after each layer (length depth + 1, the first
    entry being the starting norm before any layers are applied).
    """
    pass
