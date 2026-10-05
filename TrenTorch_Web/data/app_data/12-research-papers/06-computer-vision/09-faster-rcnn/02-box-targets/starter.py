import math


def box_targets(anchor, gt):
    """
    anchor: proposal box [x1, y1, x2, y2]
    gt: ground-truth box [x1, y1, x2, y2]

    Returns:
        The regression targets (tx, ty, tw, th) that map the anchor onto the ground-truth box.
    """
    # TODO: Convert both boxes to centers and sizes, then compute the four offsets (see Theory).
    pass
