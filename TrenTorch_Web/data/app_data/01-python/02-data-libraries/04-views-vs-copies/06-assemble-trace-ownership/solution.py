import numpy as np


def trace_pipeline(arr: np.ndarray) -> dict:
    step_a = arr[2:9]
    step_b = step_a[[0, 2, 4]]
    step_c = step_a.copy()

    step_b_before = step_b[0]
    step_c_before = step_c[0]

    step_a[0] = -1

    def ultimate_owner(a):
        current = a
        while current.base is not None:
            current = current.base
        return current

    return {
        "step_a": step_a,
        "step_b": step_b,
        "step_c": step_c,
        "arr_after_mutation": arr,
        "step_a_shares_memory_with_arr": bool(np.shares_memory(step_a, arr)),
        "step_b_shares_memory_with_arr": bool(np.shares_memory(step_b, arr)),
        "step_c_shares_memory_with_arr": bool(np.shares_memory(step_c, arr)),
        "step_a_ultimate_owner_is_arr": ultimate_owner(step_a) is arr,
        "arr_reflects_mutation": bool(arr[2] == -1),
        "step_b_reflects_mutation": bool(step_b[0] != step_b_before),
        "step_c_reflects_mutation": bool(step_c[0] != step_c_before),
    }
