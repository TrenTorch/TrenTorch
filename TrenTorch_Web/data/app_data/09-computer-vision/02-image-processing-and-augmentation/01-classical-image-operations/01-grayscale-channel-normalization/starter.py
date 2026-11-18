import numpy as np


def to_grayscale(img: np.ndarray) -> np.ndarray:
    """(H, W, 3) -> (H, W) using the luma weights 0.299, 0.587, 0.114."""
    # TODO
    pass


def normalize_channels(img: np.ndarray, mean, std) -> np.ndarray:
    """(img - mean) / std with per-channel mean and std."""
    # TODO
    pass
