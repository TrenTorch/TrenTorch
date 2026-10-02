import numpy as np


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
