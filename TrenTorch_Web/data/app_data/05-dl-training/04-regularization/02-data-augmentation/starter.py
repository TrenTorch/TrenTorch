import numpy as np


def horizontal_flip(image: np.ndarray) -> np.ndarray:
    """
    Flips `image` (shape (H, W, ...)) left-to-right along its WIDTH axis
    (axis 1). A photo of a dog mirrored left-to-right is still, obviously,
    a photo of the same dog, this is exactly what "label-preserving"
    means: the transformation changes the pixels but not the correct
    label.
    """
    pass


def random_crop(image: np.ndarray, crop_h: int, crop_w: int, rng: np.random.RandomState) -> np.ndarray:
    """
    Crops a (crop_h, crop_w) region out of `image` (shape (H, W, ...)) at
    a RANDOM valid position (chosen using `rng`, so results are
    reproducible given the same rng state), and returns just that region.
    """
    pass


def add_gaussian_noise(image: np.ndarray, std: float, rng: np.random.RandomState) -> np.ndarray:
    """
    Adds independent Gaussian noise (mean 0, standard deviation `std`) to
    every pixel of `image`, generated via `rng`.
    """
    pass
