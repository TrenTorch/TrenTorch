import numpy as np


def try_broadcast_add(a: np.ndarray, b: np.ndarray) -> dict:
    try:
        result = a + b
        return {"success": True, "result": result, "shape_a": a.shape, "shape_b": b.shape}
    except ValueError:
        return {"success": False, "result": None, "shape_a": a.shape, "shape_b": b.shape}


def find_first_incompatible_axis(shape_a: tuple, shape_b: tuple):
    length = max(len(shape_a), len(shape_b))
    padded_a = (1,) * (length - len(shape_a)) + tuple(shape_a)
    padded_b = (1,) * (length - len(shape_b)) + tuple(shape_b)

    for i in range(1, length + 1):
        a_dim = padded_a[-i]
        b_dim = padded_b[-i]
        if not (a_dim == b_dim or a_dim == 1 or b_dim == 1):
            return -i
    return None
