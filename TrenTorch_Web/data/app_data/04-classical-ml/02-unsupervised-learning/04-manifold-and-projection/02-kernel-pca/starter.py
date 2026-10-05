import numpy as np


def kernel_pca(X: np.ndarray, n_components: int, gamma=None) -> np.ndarray:
    """
    Kernel PCA scores of shape (n, n_components). gamma=None uses the linear
    kernel, otherwise an RBF kernel with that gamma. Raises ValueError for an
    out-of-range n_components or a nonpositive gamma.
    """
    pass
