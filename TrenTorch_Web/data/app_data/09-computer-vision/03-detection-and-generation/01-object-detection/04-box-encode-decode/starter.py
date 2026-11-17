import numpy as np


def encode_boxes(gt: np.ndarray, anchors: np.ndarray) -> np.ndarray:
    """Deltas [dx, dy, dw, dh] that turn each anchor into its ground-truth box."""
    # TODO
    pass


def decode_boxes(deltas: np.ndarray, anchors: np.ndarray) -> np.ndarray:
    """Apply deltas to anchors; returns boxes (x1, y1, x2, y2)."""
    # TODO
    pass
