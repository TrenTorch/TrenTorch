import numpy as np


def matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Mirrors torch.matmul(a, b), which has different rules depending on
    dimensionality (see Theory): 1D-1D dot product, 1D-2D and 2D-1D
    vector-matrix products, 2D-2D standard matrix multiplication, and
    batched matmul with leading-dimension broadcasting for higher-rank
    inputs.
    """
    # TODO: one line -- @ already implements every one of torch.matmul's
    # rules identically.
    pass
