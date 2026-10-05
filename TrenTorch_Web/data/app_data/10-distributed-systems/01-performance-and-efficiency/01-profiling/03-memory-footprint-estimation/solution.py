import numpy as np

_BYTES_PER_DTYPE = {
    "float32": 4,
    "float16": 2,
    "bfloat16": 2,
    "int8": 1,
}


def estimate_memory_bytes(params: list[np.ndarray], dtype: str = "float32") -> int:
    total_elements = sum(p.size for p in params)
    return total_elements * _BYTES_PER_DTYPE[dtype]


def estimate_optimizer_memory_bytes(
    params: list[np.ndarray], dtype: str = "float32", optimizer: str = "sgd"
) -> int:
    multiplier = {"sgd": 0, "momentum": 1, "adam": 2}[optimizer]
    param_bytes = estimate_memory_bytes(params, dtype)
    gradient_bytes = param_bytes
    optimizer_state_bytes = param_bytes * multiplier
    return param_bytes + gradient_bytes + optimizer_state_bytes
