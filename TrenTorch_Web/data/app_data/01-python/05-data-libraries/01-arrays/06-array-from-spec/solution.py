import numpy as np


def build_and_describe(spec: dict) -> dict:
    kind = spec["kind"]
    dtype = spec.get("dtype")

    if kind == "from_list":
        arr = np.array(spec["values"], dtype=dtype)
    elif kind == "zeros":
        arr = np.zeros(spec["shape"], dtype=dtype)
    elif kind == "arange":
        arr = np.arange(spec["start"], spec["stop"], spec["step"], dtype=dtype)
    elif kind == "linspace":
        arr = np.linspace(spec["start"], spec["stop"], spec["num"], dtype=dtype)
    else:
        raise ValueError(f"unknown kind: {kind}")

    return {
        "array": arr,
        "shape": arr.shape,
        "ndim": arr.ndim,
        "size": arr.size,
        "dtype": str(arr.dtype),
    }
