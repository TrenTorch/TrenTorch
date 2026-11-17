import numpy as np


def match_anchors(anchors: np.ndarray, gt_boxes: np.ndarray, pos_thresh: float, neg_thresh: float) -> np.ndarray:
    """Per-anchor assignment: gt index (>= 0), -1 for background, -2 for ignored."""
    # TODO
    pass
