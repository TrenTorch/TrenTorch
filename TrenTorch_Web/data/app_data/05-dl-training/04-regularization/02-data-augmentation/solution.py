import numpy as np


def horizontal_flip(image: np.ndarray) -> np.ndarray:
    return image[:, ::-1, ...]


def random_crop(image: np.ndarray, crop_h: int, crop_w: int, rng: np.random.RandomState) -> np.ndarray:
    height, width = image.shape[0], image.shape[1]
    top = rng.randint(0, height - crop_h + 1)
    left = rng.randint(0, width - crop_w + 1)
    return image[top : top + crop_h, left : left + crop_w]


def add_gaussian_noise(image: np.ndarray, std: float, rng: np.random.RandomState) -> np.ndarray:
    noise = rng.normal(loc=0.0, scale=std, size=image.shape)
    return image + noise
