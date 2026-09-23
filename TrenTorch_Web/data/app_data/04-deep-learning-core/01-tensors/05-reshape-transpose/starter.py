import numpy as np


def reshape(a: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    """Mirrors torch.reshape(a, shape). shape may contain one -1, inferred from the total element count."""
    pass


def transpose(a: np.ndarray, dim0: int, dim1: int) -> np.ndarray:
    """Mirrors torch.transpose(a, dim0, dim1): swaps exactly these TWO dimensions, leaves every other dimension in place."""
    pass


def permute(a: np.ndarray, dims: tuple[int, ...]) -> np.ndarray:
    """Mirrors torch.permute(a, dims): reorders ALL dimensions according to dims (a full permutation, not a two-dimension swap)."""
    pass
