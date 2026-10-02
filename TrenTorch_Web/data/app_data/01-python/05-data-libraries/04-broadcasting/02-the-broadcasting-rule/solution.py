import numpy as np


def _pad_shapes(shape_a: tuple, shape_b: tuple):
    length = max(len(shape_a), len(shape_b))
    padded_a = (1,) * (length - len(shape_a)) + tuple(shape_a)
    padded_b = (1,) * (length - len(shape_b)) + tuple(shape_b)
    return padded_a, padded_b


def are_broadcastable(shape_a: tuple, shape_b: tuple) -> bool:
    padded_a, padded_b = _pad_shapes(shape_a, shape_b)
    return all(a == b or a == 1 or b == 1 for a, b in zip(padded_a, padded_b))


def broadcast_result_shape(shape_a: tuple, shape_b: tuple) -> tuple:
    padded_a, padded_b = _pad_shapes(shape_a, shape_b)
    return tuple(max(a, b) for a, b in zip(padded_a, padded_b))
