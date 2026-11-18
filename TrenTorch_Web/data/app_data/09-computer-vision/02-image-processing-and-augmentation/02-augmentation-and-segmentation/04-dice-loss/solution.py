import numpy as np


def dice_coefficient(pred, target, eps=1e-6):
    p = np.asarray(pred, dtype=float).reshape(len(pred), -1)
    t = np.asarray(target, dtype=float).reshape(len(target), -1)
    inter = (p * t).sum(axis=1)
    return (2 * inter + eps) / (p.sum(axis=1) + t.sum(axis=1) + eps)


def dice_loss(pred, target, eps=1e-6):
    return float(1.0 - dice_coefficient(pred, target, eps).mean())
