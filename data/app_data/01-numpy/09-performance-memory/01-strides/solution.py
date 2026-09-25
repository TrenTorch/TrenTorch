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
