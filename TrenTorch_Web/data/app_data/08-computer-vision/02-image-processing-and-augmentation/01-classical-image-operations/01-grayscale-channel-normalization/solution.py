import numpy as np


def to_grayscale(img):
    return np.asarray(img, dtype=float) @ np.array([0.299, 0.587, 0.114])


def normalize_channels(img, mean, std):
    return (np.asarray(img, dtype=float) - np.asarray(mean)) / np.asarray(std)
