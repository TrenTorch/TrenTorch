import numpy as np


def conv2d_same(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """(C, H, W) * (O, C, k, k) -> (O, H, W), stride 1, zero padding k // 2, no bias."""
    # TODO
    pass


def inception_forward(x: np.ndarray, p: dict) -> np.ndarray:
    """Four parallel branches (1x1; 1x1->3x3; 1x1->5x5; maxpool->1x1) concatenated on channels."""
    # TODO
    pass
