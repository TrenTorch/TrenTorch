import numpy as np


def weighted_bce_loss(p: np.ndarray, y: np.ndarray, class_weights: dict) -> float:
    """class_weights: e.g. {0: 1.0, 1: 5.0}"""
    # TODO: Same as bce_loss, but scale each sample's loss term by its
    # class weight before averaging. Clip p away from 0/1 first.
    pass
