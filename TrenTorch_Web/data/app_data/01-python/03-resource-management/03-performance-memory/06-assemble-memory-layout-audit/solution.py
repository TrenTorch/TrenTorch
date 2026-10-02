import time

import numpy as np


def _compute_c_strides(shape: tuple, itemsize: int) -> tuple:
    strides = [0] * len(shape)
    running = itemsize
    for k in range(len(shape) - 1, -1, -1):
        strides[k] = running
        running *= shape[k]
    return tuple(strides)


def _best_time(func, repeats: int) -> float:
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)
    return min(times)


def audit_array(arr: np.ndarray, new_shape: tuple) -> dict:
    expected_c_strides = _compute_c_strides(arr.shape, arr.itemsize)
    reshape_copies = not np.shares_memory(arr, arr.reshape(new_shape))
    contiguous_version = np.ascontiguousarray(arr)
    conversion_copied = not np.shares_memory(arr, contiguous_version)

    def nested_loop_total():
        total = 0
        for row in arr:
            for value in row:
                total += value
        return total

    nested_total = nested_loop_total()
    sum_matches = bool(np.isclose(nested_total, arr.sum()))

    loop_time = _best_time(nested_loop_total, 3)
    vec_time = _best_time(arr.sum, 3)

    return {
        "strides": arr.strides,
        "expected_c_strides": expected_c_strides,
        "nbytes": arr.nbytes,
        "c_contiguous": bool(arr.flags["C_CONTIGUOUS"]),
        "reshape_copies": bool(reshape_copies),
        "contiguous_version": contiguous_version,
        "conversion_copied": bool(conversion_copied),
        "sum_matches": sum_matches,
        "speedup": loop_time / vec_time,
    }
