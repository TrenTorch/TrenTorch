import numpy as np


def cutmix_box(H: int, W: int, lam: float, cy: int, cx: int):
    """Returns (y1, y2, x1, x2) of the patch with area about (1 - lam), centred at (cy, cx) and clipped."""
    # TODO
    pass


def cutmix(img_a: np.ndarray, img_b: np.ndarray, box) -> np.ndarray:
    """Copy of img_a with the box region replaced by img_b's."""
    # TODO
    pass


def adjusted_lambda(box, H: int, W: int) -> float:
    """Fraction of the image that still comes from img_a."""
    # TODO
    pass
