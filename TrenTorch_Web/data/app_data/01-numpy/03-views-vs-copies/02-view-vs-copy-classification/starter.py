import numpy as np


def classify_operation_result(arr: np.ndarray, operation_name: str) -> str:
    """
    Given a 1D array `arr` and one of the following operation
    names, perform that operation and return either "view" or
    "copy" based on whether the result shares memory with `arr`
    (use np.shares_memory to check, do not hardcode the answer):

      "basic_slice"     -> arr[1:4]
      "fancy_index"     -> arr[[0, 2]]
      "boolean_mask"    -> arr[arr > arr.mean()]
      "arithmetic"      -> arr + 1
      "explicit_array"  -> np.array(arr)

    Return exactly "view" or "copy" based on the actual observed
    result, not from memorized rules.
    """
    pass
