import numpy as np


def count_parameters(params: list[np.ndarray]) -> int:
    return sum(p.size for p in params)


def count_trainable_parameters(params: list[np.ndarray], requires_grad: list[bool]) -> int:
    return sum(p.size for p, trainable in zip(params, requires_grad) if trainable)
