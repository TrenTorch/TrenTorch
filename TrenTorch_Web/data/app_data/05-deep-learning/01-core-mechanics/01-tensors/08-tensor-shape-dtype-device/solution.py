import numpy as np


def make_tensor_meta(arr: np.ndarray, device: str = "cpu") -> dict:
    return {"shape": arr.shape, "dtype": str(arr.dtype), "device": device}


def cast_floats_to_tensor_default(arr: np.ndarray) -> np.ndarray:
    if arr.dtype == np.float64:
        return arr.astype(np.float32)
    return arr


def check_same_device(device_a: str, device_b: str) -> None:
    if device_a != device_b:
        raise ValueError(f"devices differ: {device_a} vs {device_b}")
    return None
