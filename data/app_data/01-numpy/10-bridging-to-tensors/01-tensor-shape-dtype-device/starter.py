import numpy as np


def make_tensor_meta(arr: np.ndarray, device: str = "cpu") -> dict:
    """
    Return a dictionary describing `arr` the way a tensor's metadata
    would:
      "shape":  arr.shape (a tuple)
      "dtype":  the dtype of arr as a string, e.g. "float32"
      "device": the `device` string given
    """
    pass


def cast_floats_to_tensor_default(arr: np.ndarray) -> np.ndarray:
    """
    If `arr` has dtype float64, return a float32 version of it (a new
    array; `arr` is not modified). For every other dtype (float32,
    int64, bool, ...), return `arr` unchanged (the same array or an
    equal one is fine).
    """
    pass


def check_same_device(device_a: str, device_b: str) -> None:
    """
    Raise ValueError if `device_a` and `device_b` are different strings.
    The error message must mention both device names.
    Return None if they are the same.
    """
    pass
