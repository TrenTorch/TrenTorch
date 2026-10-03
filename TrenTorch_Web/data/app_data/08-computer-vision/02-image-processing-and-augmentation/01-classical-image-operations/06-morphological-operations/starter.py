import numpy as np


def erode(binary: np.ndarray, k: int) -> np.ndarray:
    """1 where the whole k x k window is 1 (outside the image counts as 0)."""
    # TODO
    pass


def dilate(binary: np.ndarray, k: int) -> np.ndarray:
    """1 where any pixel of the k x k window is 1."""
    # TODO
    pass


def opening(binary: np.ndarray, k: int) -> np.ndarray:
    """dilate(erode(binary, k), k)."""
    # TODO
    pass
