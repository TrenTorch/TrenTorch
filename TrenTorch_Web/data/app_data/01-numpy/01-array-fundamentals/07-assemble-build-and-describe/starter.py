import numpy as np


def build_and_describe(spec: dict) -> dict:
    """
    `spec` is a dictionary describing how to build an array, in
    one of these forms:

      {"kind": "from_list", "values": [...], "dtype": <dtype or None>}
      {"kind": "zeros", "shape": (...), "dtype": <dtype or None>}
      {"kind": "arange", "start": ..., "stop": ..., "step": ..., "dtype": <dtype or None>}
      {"kind": "linspace", "start": ..., "stop": ..., "num": ..., "dtype": <dtype or None>}

    Build the array according to `spec["kind"]`, applying
    `spec["dtype"]` explicitly if it is not None.

    Return a dictionary:
      {
        "array": <the built ndarray>,
        "shape": <its shape>,
        "ndim": <its ndim>,
        "size": <its size>,
        "dtype": <its dtype, as a string>
      }
    """
    pass
