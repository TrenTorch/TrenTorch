import numpy as np


def flatten(image: np.ndarray) -> np.ndarray:
    return image.reshape(-1)
