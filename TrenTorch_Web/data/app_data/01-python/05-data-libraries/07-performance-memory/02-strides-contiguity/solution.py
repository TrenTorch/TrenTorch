import numpy as np


def compute_c_strides(shape: tuple, itemsize: int) -> tuple:
    strides = [0] * len(shape)
    running = itemsize
    for k in range(len(shape) - 1, -1, -1):
        strides[k] = running
        running *= shape[k]
    return tuple(strides)


def byte_offset(index: tuple, strides: tuple) -> int:
    return sum(i * s for i, s in zip(index, strides))


def slice_step_strides(arr: np.ndarray, step: int) -> tuple:
    return (arr.strides[0] * step,) + arr.strides[1:]


def contiguity_flags(arr: np.ndarray) -> dict:
    return {
        "c_contiguous": bool(arr.flags["C_CONTIGUOUS"]),
        "f_contiguous": bool(arr.flags["F_CONTIGUOUS"]),
    }


def contiguity_of_ops(arr: np.ndarray) -> dict:
    return {
        "row_slice": bool(arr[1:3].flags["C_CONTIGUOUS"]),
        "column_slice": bool(arr[:, 0].flags["C_CONTIGUOUS"]),
        "step_slice": bool(arr[::2].flags["C_CONTIGUOUS"]),
        "transpose": bool(arr.T.flags["C_CONTIGUOUS"]),
        "transpose_copy": bool(arr.T.copy().flags["C_CONTIGUOUS"]),
    }
