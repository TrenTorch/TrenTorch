import numpy as np


def partial_derivative(f, x: np.ndarray, index: int, eps: float = 1e-5) -> float:
    """
    f takes a vector x and returns a scalar. The partial derivative
    with respect to x[index] holds every OTHER coordinate fixed and
    measures how f changes as only that one coordinate moves, using
    01-derivatives-first-principles' central difference formula along
    just that one axis:

        df/dx_index ~= (f(x with x[index]+eps) - f(x with x[index]-eps)) / (2*eps)
    """
    pass


def gradient(f, x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """
    The gradient is simply the vector of ALL partial derivatives, one
    per coordinate of x:

        gradient(f, x)[i] = partial_derivative(f, x, i)
    """
    pass
