import numpy as np


def classify_operation_result(arr: np.ndarray, operation_name: str) -> str:
    operations = {
        "basic_slice": lambda a: a[1:4],
        "fancy_index": lambda a: a[[0, 2]],
        "boolean_mask": lambda a: a[a > a.mean()],
        "arithmetic": lambda a: a + 1,
        "explicit_array": lambda a: np.array(a),
    }
    result = operations[operation_name](arr)
    return "view" if np.shares_memory(result, arr) else "copy"
