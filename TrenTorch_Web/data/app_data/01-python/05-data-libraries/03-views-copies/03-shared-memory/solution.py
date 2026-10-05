import numpy as np


def zero_out_via_view(arr: np.ndarray, start: int, stop: int) -> None:
    view = arr[start:stop]
    view[:] = 0


def chained_view_mutation(arr: np.ndarray) -> dict:
    view1 = arr[1:7]
    view2 = view1[2:5]
    view2[:] = -1
    return {"arr": arr, "view1": view1, "view2": view2}


def get_independent_slice(arr: np.ndarray, start: int, stop: int) -> np.ndarray:
    return arr[start:stop].copy()


def safe_modify_first_n(arr: np.ndarray, n: int, new_value) -> np.ndarray:
    result = arr.copy()
    result[:n] = new_value
    return result
